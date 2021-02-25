from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .bodyClasses import AuthorBody, StoryBody
from .models import Story, Author
from datetime import date, datetime
from .forms import LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import json
import uuid

storyTableName = "cw1app_story"
dateTimeFormat = "%d/%m/%Y"
contentTypePlainText = "text/plain"
contentTypeAppJson = "application/json"
unauthenticatedUser = "AnonymousUser"

@csrf_exempt
def login_author(req):
    if req.method == "POST":
        form = LoginForm(req.POST)
        if form.is_valid():
            suppliedUsername = form.cleaned_data["username"]
            suppliedPassword = form.cleaned_data["password"]

            user = authenticate(
                req, username=suppliedUsername, password=suppliedPassword
            )

            if user is not None:
                login(req, user)
                return HttpResponse(
                    content="Login Successful", status=200, content_type=contentTypePlainText
                )
            else:
                return HttpResponse(
                    content="Incorrect username or password",
                    status=401,
                    content_type=contentTypePlainText,
                )
        else:
            return HttpResponse(
                content="Error logging in. Has all data been submitted?",
                status=401,
                content_type=contentTypePlainText,
            )
    else:
        return HttpResponseNotAllowed(permitted_methods=["POST"])


@login_required
@csrf_exempt
def logout_author(req):
    if req.method == "POST":
        logout(req)
        resp = HttpResponse(
            content="Logged out", status=200, content_type=contentTypePlainText
        )
        resp.delete_cookie('sessionid')
        return resp
    else:
        return HttpResponseNotAllowed(permitted_methods=["POST"])


# We cannot use @login_required as we want a custom error message.
@csrf_exempt
def post_story(req):
    if req.method == "POST":
        if str(req.user) == unauthenticatedUser:
            return HttpResponse(
                content="Must be logged in to perform this operation",
                status=503,
                content_type=contentTypePlainText,
            )
        jsonBody = json.loads(req.body)
        today = (
            date.today()
        )  # We want to re-evaluate this every time the function is called in case a new day has started

        # Extract fields
        key = uuid.uuid4()
        headline = jsonBody["headline"]
        category = jsonBody["category"]
        region = jsonBody["region"]
        details = jsonBody["details"]
        dateSubmitted = today.strftime(dateTimeFormat)

        # Create story
        story = StoryBody(
            key, headline, category, region, req.user, dateSubmitted, details
        )

        # Obtain author row
        authorRow = Author.objects.get(username=story.author)

        # Insert new row
        Story(
            key=story.key,
            headline=story.headline,
            category=story.story_cat,
            region=story.story_region,
            author=authorRow,
            date=story.story_date,
            details=story.story_details,
        ).save()

        return HttpResponse(
            content="Created story", status=201, content_type=contentTypePlainText
        )
    else:
        return HttpResponseNotAllowed(permitted_methods=["POST"])

# We cannot use @login_required as we want a custom error message.
@csrf_exempt
def delete_story(req):
    if req.method == "POST":
        if str(req.user) == unauthenticatedUser:
            return HttpResponse(
                content="Must be logged in to perform this operation",
                status=503,
                content_type=contentTypePlainText,
            )
        
        jsonBody = json.loads(req.body)
        key = jsonBody["story_key"]

        try:
            Story.objects.get(key=key).delete()
        except Exception:
            return HttpResponse(
                content="Error deleting story. Does it exist?",
                status=503,
                content_type=contentTypePlainText,
            )   

        return HttpResponse(
                content=f"Deleted story with id {key}",
                status=201,
                content_type=contentTypePlainText,
            )
    else:
        return HttpResponseNotAllowed(permitted_methods=["POST"])

@csrf_exempt
def get_stories(req):
    if req.method == "GET":
        jsonBody = json.loads(req.body)
        category = jsonBody["story_cat"]
        region = jsonBody["story_region"]
        date = jsonBody["story_date"]

        # Filters are lazy, so we can chain them with no performance degredation
        stories = Story.objects.all()

        if category != "*":
            stories = stories.filter(category=category)
        if region != "*":
            stories = stories.filter(region=region)
        if date != "*":
            stories = stories.filter(date__gte=datetime.strptime(date, dateTimeFormat))

        # Create story objects from DB rows
        storyResults = []

        for story in stories:
            author = story.author.username
            date = str(story.date)

            storyResults.append(
                StoryBody(
                    story.key,
                    story.headline,
                    story.category,
                    story.region,
                    author,
                    date,
                    story.details,
                ).__dict__
            )

        # Create response
        resJson = json.dumps({"stories": storyResults})

        response = (
            HttpResponse(
                content="No stories found",
                status=404,
                content_type=contentTypePlainText,
            )
            if storyResults == []
            else HttpResponse(
                content=resJson, status=200, content_type=contentTypeAppJson
            )
        )
        return response
    else:
        return HttpResponseNotAllowed(permitted_methods=["GET"])
