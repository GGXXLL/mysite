from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, F
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Post, Comment, Part, Examine


class PostIndexView(generic.ListView):
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


class PostSelfView(LoginRequiredMixin, generic.ListView):
    template_name = 'posts/index.html'
    context_object_name = 'post_list'
    paginate_by = 10

    def get_queryset(self):
        """Return the last five published questions."""
        res = Post.objects.filter(
            pub_date__lte=timezone.now(),
            author=self.request.user,
            is_delete=False,
        )
        part = self.request.GET.get("part", "")
        if part != "":
            res = res.filter(part=part)
        q = self.request.GET.get("q", "")
        if q != "":
            res = res.filter(title__contains=q)
        return res.order_by('-edit_date')

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
        context["title"] = "我的帖子"
        return context


class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'posts/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Post.objects.filter(
            Q(
                pub_date__lte=timezone.now(),
                examine=Examine.PASS,
                is_delete=False, ) |
            Q(author=self.request.user, is_delete=False)
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
            author=self.request.user,
        )

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['part_list'] = Part.objects.all()
    #     return context


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    template_name = 'posts/edit.html'
    fields = ['part', 'title', 'text', ]
    success_url = '/posts/self/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


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


@login_required()
def vote(request, pk, up_id):
    if up_id not in (1, 2):
        return HttpResponseBadRequest()
    question = get_object_or_404(Post, pk=pk)
    if up_id == 1:
        question.agree_count = F('agree_count') + 1
    if up_id == 2:
        question.disagree_count = F('disagree_count') + 1
    question.save()

    return HttpResponseRedirect(reverse("posts:posts"))
