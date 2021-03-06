from django.contrib import admin

# Register your models here.
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin

from house.models import Category, House, Images, Comment


class HouseImageInline(admin.TabularInline):
    model = Images
    extra = 6


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    list_filter = ['status']


class HouseAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'rent', 'image_tag', 'status']
    readonly_fields = ('image_tag',)
    list_filter = ['status', 'category']
    inlines = [HouseImageInline]
    prepopulated_fields = {'slug': ('title',)}


class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'house', 'image_tag']
    readonly_fields = ('image_tag',)


class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_houses_count', 'related_houses_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative houses count
        qs = Category.objects.add_related_count(
                qs,
                House,
                'category',
                'houses_cumulative_count',
                cumulative=True)

        # Add non cumulative houses count
        qs = Category.objects.add_related_count(qs,
                 House,
                 'category',
                 'houses_count',
                 cumulative=False)
        return qs

    def related_houses_count(self, instance):
        return instance.houses_count
    related_houses_count.short_description = 'Related houses (for this specific category)'

    def related_houses_cumulative_count(self, instance):
        return instance.houses_cumulative_count
    related_houses_cumulative_count.short_description = 'Related houses (in tree)'


class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject', 'comment', 'house', 'user', 'status']
    list_filter = ['status']


admin.site.register(Category, CategoryAdmin2)
admin.site.register(House, HouseAdmin)
admin.site.register(Images, ImagesAdmin)
admin.site.register(Comment, CommentAdmin)
