#! coding: utf-8
from django.conf import settings
from django.contrib.auth.models import User, check_password
from lxml import etree
from django.contrib.auth.models import Group

class NMailAuthentication(object):
    def authenticate(self, username=None, password=None):

        url = "http://bases.bireme.br/cgi-bin/wxis1660/dic/common/scripts/wxis/"
        url += "?IsisScript=search.xis&database=/home/bases/title-nmail/nmail&search="
        url += username

        try:

            user = User.objects.get(username=username)
            try:
                if check_password(password, user.password):
                    return user
            except:
                pass

        except User.DoesNotExist:
            pass

        xml = etree.parse(url)
        root = xml.getroot()

        for item in root:
            if 'document' in item.tag:
                
                cod = item.find('codId').find('occ').text
                if username == cod and password == cod:

                    try:
                        user = User.objects.get(username=username)

                    except User.DoesNotExist: 

                        # if user doesn't exists, create an user
                        user = User(username=username, password=username)
                        user.is_staff = True
                        
                        # giving institution name
                        institution = item.find('institution').find('occ').get('a')
                        if institution:
                            user.first_name = institution
                        
                        # adding email
                        email = item.find('mail').find('occ').text
                        if email:
                            user.email = email
                        
                        user.save()
                        
                        # adding the user to group users
                        try:
                            group = Group.objects.get(name="users")
                        except:
                            group = Group(name="users")
                            group.save()
                        group.user_set.add(user)
                        
                    return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None