import graphene
from graphene_django import DjangoObjectType

from .models import Link
from users.schema import UserType
from links.models import Link, Vote
from graphql import GraphQLError

class LinkType(DjangoObjectType):
    class Meta:
        model = Link

class VoteType(DjangoObjectType):
    class Meta:
        model = Vote
        
class CreateVote(graphene.Mutation):
    user = graphene.Field(UserType)
    link = graphene.Field(LinkType)

    class Arguments:
        link_id = graphene.Int()

    def mutate(self, info, link_id):
        user = info.context.user
        if user.is_anonymous:
            #1
            raise GraphQLError('You must be logged to vote!')

        link = Link.objects.filter(id=link_id).first()
        if not link:
            raise Exception('Invalid Link!')

        Vote.objects.create(
            user=user,
            link=link,
        )

        return CreateVote(user=user, link=link)
    
class Query(graphene.ObjectType):
    links = graphene.List(LinkType)
    votes = graphene.List(VoteType)
    
    def resolve_links(self, info, **kwargs):
        return Link.objects.all()
    
    def resolve_votes(self, info, **kwargs):
        return Vote.objects.all()
    
# ...code
#1


class CreateLink(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()
    description = graphene.String()
    image = graphene.String()
    posted_by = graphene.Field(UserType)
    
    #2
    class Arguments:
        name = graphene.String()
        description = graphene.String()
        image = graphene.String()

    #3
    def mutate(self, info, name, description, image):
        user = info.context.user or None
        
        link = Link(
            name=name, 
            description=description, 
            image=image, 
            posted_by=user,
        )
        link.save()

        return CreateLink(
            id=link.id,
            name=link.name,
            description=link.description,
            image=link.image,
            posted_by=link.posted_by
        )


class UpdateLink(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()
    description = graphene.String()
    image = graphene.String()
    posted_by = graphene.Field(UserType)

    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()
        description = graphene.String()
        image = graphene.String()

    def mutate(self, info, id, name=None, description=None, image=None):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You must be logged in to update a link!')

        try:
            link = Link.objects.get(pk=id)
        except Link.DoesNotExist:
            raise GraphQLError('Link not found!')

        # Actualizar solo los campos que se proporcionan
        if name:
            link.name = name
        if description:
            link.description = description
        if image:
            link.image = image

        link.save()

        return UpdateLink(
            id=link.id,
            name=link.name,
            description=link.description,
            image=link.image,
            posted_by=link.posted_by
        )


#4
class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()
    create_vote = CreateVote.Field()
    update_link = UpdateLink.Field()