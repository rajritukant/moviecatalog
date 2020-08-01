from django.contrib import admin

# Register your models here.
from .models import Collection, Movie, Genre


class MoviesInline(admin.TabularInline):
    model = Movie.collection.through


class GenresInline(admin.TabularInline):
    model = Genre.movie.through


class CollectionAdmin(admin.ModelAdmin):
    model = Collection
    inlines = [
        MoviesInline,
    ]
    list_display = ('id', 'title', 'description', 'user',)
    # readonly_fields = ('id', 'title', 'description', 'user',)
    # fields = ('id', 'title', 'description', 'user',)

    # def has_add_permission(self, request,obj=None):
    #     return True
    # def has_delete_permission(self, request,obj=None):
    #     return False
    # def has_change_permission(self, request,obj=None):
    #     return True


class MovieAdmin(admin.ModelAdmin):
    model = Movie
    inlines = [
        GenresInline
    ]
    list_display = ('id', 'title', 'description',)
    # readonly_fields = ('id', 'title', 'description', 'collection',)
    # fields = ('id', 'title', 'description', 'collection',)


class GenreAdmin(admin.ModelAdmin):
    model = Genre
    list_display = ('id', 'name',)


admin.site.register(Collection, CollectionAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Genre, GenreAdmin)
