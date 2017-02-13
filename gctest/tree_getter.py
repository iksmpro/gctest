from .models import TreeElement
 
class TemplateObject:
    def __init__(self,*largs):
        self.name, self.has_children, self.children, self.link = largs 

def get_tree(menu, path):
    if ('/%s/'%menu) not in path:
        path = '/%s/'%menu
    path_parts = (path[:-1] if path[-1] == '/' else path).split('/')
    if not all(path_parts[1:]) or len(path_parts) == 1:
        return {'tree_elems': menu, 'error':"Incorect path here"}
    path_parts[0] = 'base_tree_element'  # path_parts = 'base_tree_element', *path_parts
    items = list(TreeElement.objects.filter(parent__in=TreeElement.objects.only('id').filter(name__in=path_parts)).all())  # one db request
    tree_elems = TemplateObject('base_tree_element',False,[],'/')
    cur_target = tree_elems
    orm_list = []
    names = []
    for part in path_parts:
        if orm_list:
            childs = [child for child in cur_target.children if child.name == part]
            if len(childs) != 1:
                return {'tree_elems': menu, 'error':"Incorect path here"}
            cur_target = childs[0]
            names.append(part)
        target = [
            i for i in items
            if i.name == part and (
                orm_list and i.parent_id==orm_list[-1].id
                or
                not orm_list and i.parent_id == i.id
            )
        ]
        if len(target) != 1:
            return {'tree_elems': menu, 'error':"Incorect path here"}
        target = target[0]
        orm_list.append(target)
        cur_target.children.extend(
            TemplateObject(i.name, False, [], '/'.join([''] + names + [i.name]))
            for i in items
            if i.parent_id==target.id and i.id != target.id
        )
        if cur_target.children:
            cur_target.has_children = True
        orm_list.append(target)
    tree_elems = [elem for elem in tree_elems.children if elem.name == path_parts[1]][0]
    return {'tree_elems': tree_elems, 'has_menu': bool(tree_elems)}