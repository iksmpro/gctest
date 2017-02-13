from django.contrib import admin
from django.db import connection

from .models import TreeElement

class AddTreeElem(admin.ModelAdmin):
    fields = ['name', 'parent']

def create_base_element(): # hack to create initial element
    with connection.cursor() as cursor:
        cursor.execute('''
            INSERT INTO "gctest_treeelement"
            ("id", "name", "parent_id") 
            values
            (1,"base_tree_element",1);
        ''')
        row = cursor.fetchone()

admin.site.register(TreeElement, AddTreeElem)  # admin password is trueAdmin123

try:
    if not list(TreeElement.objects.all()):
        create_base_element()
except:
    pass