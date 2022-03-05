from django.shortcuts import render

# Create your views here.

from .models import Book, Author, BookInstance, Genre


def index(request):
    """
    Function view of the site's homepage
    """
    # Generating the number of some main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()

    # Check yourself task
    num_genres_contain_french = Genre.objects.filter(name__contains='french').count()
    num_books_contain_watch = Book.objects.filter(title__contains='watch').count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_books_contain_watch': num_books_contain_watch,
        'num_genres_contain_french': num_genres_contain_french,
        'num_visits': num_visits
    }

    # HTML-pattern rendering in index.html with data inside
    # passed by variable context
    return render(request, 'index.html', context=context)


# Пока не понятно что
from django.views import generic


class BookListView(generic.ListView):
    model = Book
    paginate_by = 3


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author


class AuthorDetailView(generic.DetailView):
    model = Author


from django.contrib.auth.mixins import LoginRequiredMixin


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based viev listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


from django.contrib.auth.mixins import PermissionRequiredMixin


class LibrarianBorrowedBooksListView(PermissionRequiredMixin, generic.ListView):
    """Generic class based view listing books on loan to librarian."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_librarian.html'
    permission_required = 'catalog.can_mark_returned'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


