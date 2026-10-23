
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Question, Choice, Submission


@login_required
def submit(request, question_id):
    if request.method != "POST":
        return HttpResponse("Invalid request method.", status=405)

    question = get_object_or_404(Question, pk=question_id)
    choice_id = request.POST.get("choice")

    if not choice_id:
        return HttpResponse("Please select an answer.", status=400)

    choice = get_object_or_404(
        Choice,
        pk=choice_id,
        question=question
    )

    Submission.objects.create(
        user=request.user,
        question=question,
        choice=choice
    )

    return render(
        request,
        "onlinecourse/submission_confirmation.html",
        {"question": question, "choice": choice}
    )


@login_required
def show_exam_result(request, course_id):
    questions = Question.objects.filter(lesson__course_id=course_id)
    submissions = Submission.objects.filter(
        user=request.user,
        question__in=questions
    )

    correct_count = sum(
        1 for submission in submissions
        if submission.choice and submission.choice.is_correct
    )

    total_questions = questions.count()

    score = (
        round(correct_count / total_questions * 100)
        if total_questions else 0
    )

    context = {
        "correct_count": correct_count,
        "total_questions": total_questions,
        "score": score,
        "submissions": submissions,
    }

    return render(
        request,
        "onlinecourse/exam_result.html",
        context
    )
