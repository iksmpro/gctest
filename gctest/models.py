from django.db import models
from django.contrib import admin


class TreeElement(models.Model):
    name = models.CharField(max_length=256)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True)  # IntegerField()#

    def tree_name(self):
        if hasattr(self, '__tree_name'):
            return self.__tree_name
        else:
            path = [self]
            while path[-1].parent_id != path[-1].id:
                path.append(path[-1].parent)
            self.__tree_name = '/' + '/'.join(o.name for o in path[::-1][1:])  # ([self] + list(takewhile(lambda obj: obj.parent_id != obj.id, accumulate(cycle([self]), func=lambda s,_: s.parent))))[-1].name
            return self.__tree_name

    def __str__(self):
        return "{name}<{id}> ({tree})".format(name=self.name, id=self.id, tree=self.tree_name())
