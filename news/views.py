from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404,HttpResponseRedirect
import datetime as dt
from django.contrib.auth.decorators import login_required

from .models import Article, NewsLetterRecipients
from .forms import NewsLetterForm, NewArticleForm
from .email import send_welcome_email

# Create your views here.

def root(request):
    return HttpResponse('This is the home page') # Not in the LMS

# Getting news of the day
def news_today(request):
    date = dt.date.today()
    news = Article.today_news()

    if request.method == 'POST':
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['your_name']
            email = form.cleaned_data['email']

            recipient = NewsLetterRecipients(name = name, email = email)
            recipient.save()

            send_welcome_email(name, email)
            
            HttpResponseRedirect('news_today')
    else:
        form = NewsLetterForm()

    return render(request, 'all-news/today-news.html', {"date": date, "news": news, "letterForm": form})

    # Getting day of the week
    # return render(request, 'all-news/today-news.html', {"date": date,})

# Getting days of the week

'''
def convert_dates(dates):
    # Function that gets the weekday number for the date.

    day_number = dt.date.weekday(dates)

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # Returning the actual day of the week
    day = days[day_number]

    return day
'''

# Getting past news

def past_days_news(request, past_date):
    try:
        # Convert data from the string Url
        date = dt.datetime.strptime(past_date, '%Y-%m-%d').date()
    except ValueError:
        # Raise 404 error when ValueError is thrown
        raise Http404()
        assert False
    
    if date == dt.date.today():
        return redirect(news_today)
    
    news = Article.days_news(date)
    
    return render(request, 'all-news/past-news.html', {"date": date, "news": news})

def search_results(request):
    if 'article' in request.GET and request.GET["article"]:
        search_term = request.GET.get("article")
        searched_articles = Article.search_by_title(search_term)
        message = f"{search_term}"

        return render(request, 'all-news/search.html', {"message": message, "article":searched_articles})
    
    else:
        message = "You haven't searched for any term"
        return render(request, 'all-news/search.html', {"message": message})

@login_required(login_url='/accounts/login/')
def article(request, article_id):
    try:
        article = Article.objects.get(id = article_id)
    except DoesNotExist:
        raise Http404()
    
    return render(request, "all-news/article.html", {"article": article})

@login_required(login_url='/account/login/')
def new_article(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.editor = current_user
            article.save()
        return redirect(news_today)
    
    else:
        form = NewArticleForm()
    
    return render(request, 'new_article.html', {"form": form})