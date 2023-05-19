##Controle de Preço VTEX!!!



##Execução do projeto


<br>criar venv: py -3 -m venv venv<br/>
<br>ativar: venv\Scripts\activate<br/>
<br>instalar dependencias: pip freeze > requirements.txt<br/>
<br>$env:FLASK_APP = "app:create_app()"<br/>


#Migrações banco de dados

<br>flask db init<br/>
<br>flask db migrate -m "Initial migration."<br/>
<br>flask db upgrade<br/>

<br>flask run --host=0.0.0.0<br/>


<br>flask db stamp head</br>


