# -*- coding: utf-8 -*-
from datetime import datetime


def get_first_name():
    name = 'Nobody'
    if auth.user:
        name = auth.user.first_name
    return name

CATEGORY = ['Car', 'Bike', 'Books', 'Music', 'Outdoors', 'For the house', 'Misc.']

db.define_table('samslist',
                Field('user_id', db.auth_user),
                Field('name'),
                Field('phone'),
                Field('email'),
                Field('title', unique=True),
                Field('category'),
                Field('price'),
                Field('available', 'boolean'),
                Field('date_posted', 'datetime'),
                Field('description', 'text'),
                Field('image', 'upload'),
                )

db.samslist.id.readable = False
db.samslist.description.label = 'Description'
db.samslist.name.default = get_first_name()
db.samslist.date_posted.default = datetime.utcnow()
db.samslist.name.writable = False
db.samslist.date_posted.writable = False
db.samslist.user_id.default = auth.user_id
db.samslist.user_id.writable = db.samslist.user_id.readable = False
db.samslist.email.requires = IS_EMAIL()
db.samslist.category.requires = IS_IN_SET(CATEGORY)
db.samslist.category.default = 'Misc'
db.samslist.category.required = True
db.samslist.price.required = True
db.samslist.image.requires = IS_IMAGE(error_message="Oops! That's not an image file.")


""" db.define_table('bboard',
                Field('name'),
                Field('user_id', db.auth_user),
                Field('phone'),
                Field('email'),
                Field('category'),
                Field('date_posted', 'datetime'),
                Field('title'),
                Field('bbmessage', 'text'),
                )

db.bboard.id.readable = False
db.bboard.bbmessage.label = 'Message'
db.bboard.name.default = get_first_name()
db.bboard.date_posted.default = datetime.utcnow()
db.bboard.name.writable = False
db.bboard.date_posted.writable = False
db.bboard.user_id.default = auth.user_id
db.bboard.user_id.writable = db.bboard.user_id.readable = False
db.bboard.email.requires = IS_EMAIL()
db.bboard.category.requires = IS_IN_SET(CATEGORY)
db.bboard.category.default = 'Misc'
db.bboard.category.required = True """
