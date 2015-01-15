# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - api is an example of Hypermedia API support and access control
#########################################################################
    
def index():
    """Better index."""
    # Let's get all data. 
    q = db.bboard
    
    def generate_del_button(row):
        # If the record is ours, we can delete it.
        b = ''
        if auth.user_id == row.user_id:
            b = A('Delete', _class='btn', _href=URL('default', 'delete', args=[row.id]))
        return b
    
    def generate_edit_button(row):
        # If the record is ours, we can delete it.
        b = ''
        if auth.user_id == row.user_id:
            b = A('Edit', _class='btn', _href=URL('default', 'edit', args=[row.id]))
        return b

    def shorten_post(row):
        return row.bbmessage[:10] + '...'

    # Creates extra buttons.

    links = [
        dict(header='', body = generate_del_button),
        dict(header='', body = generate_edit_button),
        ]

    if len(request.args) == 0:
        # We are in the main index.
        links.append(dict(header='Post', body = shorten_post))
        db.bboard.bbmessage.readable = False

    form = SQLFORM.grid(q,
        fields=[db.bboard.user_id, db.bboard.date_posted, 
                db.bboard.category, db.bboard.title, 
                db.bboard.bbmessage],
        editable=False, deletable=False,
        links=links,
        paginate=2,
        )
    return dict(form=form)


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_login() 
def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection
    rules = {
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        }
    return Collection(db).process(request,response,rules)
