import graphene
from graphene import relay

from graphene_django import DjangoObjectType

from .models import Ingredient, Category
# subclass DjangoObjectType if using django models 

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ('id', 'name', 'ingredients')

class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'notes', 'category')
        
# class Ship(graphene.ObjectType):
#     class Meta:
#         interfaces = (relay.Node, )

#     name = graphene.String(description='The name of the ship')

#     @classmethod
#     def get_node(cls, info, id):
#         return get_ship(id)

#     @staticmethod
#     def to_global_id(type_, id):
#         # to_global_id will define how a node id is encoded
#         return f'{type_}:{id}'

#     @staticmethod
#     def get_node_from_global_id(info, global_id, only_type=None):
#         # get_node_from_global_id how to retriee a Node given a encoded id
#         type_, id = global_id.split(':')
#         if only_type:
#             # we assure that the node type that we want to retrieve
#             # is the same that was indicated in the field type
#             assert type_ == only_type._meta.name, 'Received not compatible node.'

#         if type_ == 'User':
#             return get_user(id)
#         elif type_ == 'Photo':
#             return get_photo(id)

# Root type while all access begins
class Query(graphene.ObjectType):
    all_ingredients = graphene.List(IngredientType)
    category_by_name = graphene.Field(CategoryType, name=graphene.String(required=True))

    # Should be CustomNode.Field() if we want to use our ccustom Node
    
    node = relay.Node.Field()

    def resolve_all_ingredients(root, info):
        # we can easily optimize query count in the resolve method
        return Ingredient.objects.select_related('category').all()
    
    def resolve_category_by_name(root, info, name):
        try:
            return Category.objects.get(name=name)
        except Category.DoesNotExist:
            return None


class CreateCategory(graphene.Mutation):

    class Arguments:
        name = graphene.String(required=True)

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, name):
        category = Category(name=name)
        category.save()
        return CreateCategory(category=category)


class Mutation(graphene.ObjectType):
    update_category = CreateCategory.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)

