from django.contrib import admin
from django.forms import BaseInlineFormSet
from django.core.exceptions import ValidationError

from .models import Article, Tag, Scope

class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        is_main_count = 0

        for form in self.forms:
            if form.cleaned_data.get('is_main', False) == True:
                if is_main_count:
                    raise ValidationError('Основным может быть только один раздел')
                is_main_count += 1
        if not is_main_count:
            raise ValidationError('Укажите основной раздел')
        
        return super().clean()

class ScopeInline(admin.TabularInline):
    model = Scope
    extra = 1
    formset = ScopeInlineFormset

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'published_at']
    inlines = [ScopeInline]

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']