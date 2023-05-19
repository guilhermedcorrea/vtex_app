from flask import Flask,Blueprint, current_app,redirect,session
from flask_sqlalchemy import SQLAlchemy 
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin import AdminIndexView
from flask_admin.model.template import EndpointLinkRowAction, LinkRowAction
from flask_admin.model import BaseModelView
from flask_admin.base import BaseView, expose
from flask_admin.menu import MenuLink
from flask_sqlalchemy import model
from flask_admin import tools

from os.path import dirname, join


from ..models.models import Usuario, Precos,Produto
from ..extensions import db,admin


vtex = Blueprint("api",__name__)

@vtex.route("/")
def index():
    teste = Precos.query.all()
    
    print(teste)
    return redirect("/admin")

class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def Home(self):
     
        return self.render('admin/index.html')


admin = Admin(current_app, name='Admin',
              template_mode='bootstrap3', index_view=MyAdminIndexView())

current_app.config['FLASK_ADMIN_FLUID_LAYOUT'] = True


'''
class MyModelView(BaseModelView):
    column_extra_row_actions = [
        LinkRowAction('glyphicon glyphicon-off', 'http://direct.link/?id={row_id}'),
        EndpointLinkRowAction('glyphicon glyphicon-test', 'my_view.index_view')
    ]
'''   
 
class UserView(ModelView):
    column_exclude_list = []
    column_display_pk = True
    can_create = True
    can_edit = True
    can_delete = False
    can_export = True
    



class ProdutosView(ModelView):
    can_set_page_size = True
    page_size = 20
    create_modal = True
    can_create = True
    can_edit = True
    can_delete = False
    can_export = True

    column_display_pk = True
    column_searchable_list = ['skuid','id_listapreco','nome_produto']
    can_view_details = True
    column_list = ['cod_produto', 'nome_produto',
                   'preco_lista', 'preco', 'ref_marca', 'trade_policy']

    column_filters = [

        'skuid','id_listapreco','nome_produto'

    ]
        
    def get_one(self, id):
        produtos = Produto.query.filter_by(cod_produto=id).first()
        produtos = {
            "id":produtos.cod_produto,
            "nome_produto":produtos.nome_produto,
            "preco_lista":produtos.preco_lista,
            "preco":produtos.preco,
            "ref_marca":produtos.ref_marca,
            "trade_policy":produtos.trade_policy,
            "skuid":produtos.skuid,
            "id_listapreco":produtos.skuid}
        print(produtos)
        return self.session.query(self.model).get(tools.iterdecode(id))
    
class PrecosView(ModelView):
    page_size = 20
    column_exclude_list = []
    column_display_pk = True
    can_create = True
    can_edit = True
    can_delete = False
    can_export = True


class CommentView(ModelView):
    create_modal = True

class NotificationsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/notification.html')


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment_text = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Comment %r>' % (self.id)

admin.add_view(NotificationsView(name='Notificações', endpoint='notify'))


admin.add_view(UserView(Usuario, db.session))

admin.add_view(ProdutosView(Produto, db.session))

admin.add_view(PrecosView(Precos, db.session))


admin.add_view(FileAdmin(r'C:\vtex_app\app\uploads', name='Uploads'))
