from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Post, Comment, Part, Examine


class PostIndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'posts/index.html'
    context_object_name = 'post_list'
    paginate_by = 10

    def get_queryset(self):
        """Return the last five published questions."""
        res = Post.objects.filter(
            pub_date__lte=timezone.now(),
            examine=Examine.PASS,
            is_delete=False,
        )
        part = self.request.GET.get("part", "")
        if part != "":
            res = res.filter(part=part)
        q = self.request.GET.get("q", "")
        if q != "":
            res = res.filter(title__contains=q)

        return res.order_by('-pub_date')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['part_list'] = Part.objects.all()
        extra_args = ""
        part = self.request.GET.get("part", 0)
        context['select_part'] = Part.objects.filter(pk=part).first()
        if part:
            extra_args += f"&part={part}"
        q = self.request.GET.get("q", "")
        if q != "":
            extra_args += f"&q={q}"
        context['extra_args'] = extra_args
        return context


class PostDetailView(LoginRequiredMixin, generic.DetailView):
    model = Post
    template_name = 'posts/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Post.objects.filter(
            pub_date__lte=timezone.now(),
            examine=Examine.PASS,
            is_delete=False,
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['part_list'] = Part.objects.all()
        return context


class PostEditView(LoginRequiredMixin, generic.UpdateView):
    model = Post
    template_name = 'posts/edit.html'
    fields = ['title', 'text']

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Post.objects.filter(
            pub_date__lte=timezone.now(),
            examine=Examine.PASS,
            is_delete=False,
        )

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['part_list'] = Part.objects.all()
    #     return context


class CommentsView(LoginRequiredMixin, generic.DetailView):
    model = Comment

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Comment.objects.filter(
            pub_date__lte=timezone.now(),
            examine=Examine.PASS,
            is_delete=False,
        )


class PartView(LoginRequiredMixin, generic.ListView):
    def get_queryset(self):
        """Return the last five published questions."""
        return Part.objects.all()

# @login_required()
# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(request, 'posts/detail.html', {
#             'question': question,
#             'error_message': "You didn't select a choice.",
#         })
#     else:
#         selected_choice.votes = F('votes') + 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse('posts:results', args=(question.id,)))
