## ZSSN
O mundo como o conheceu caiu em um cenário apocalíptico. Um vírus produzido em laboratório está transformando seres humanos e animais em zumbis, famintos por carne fresca. o ZSSN é uma API designada para desenvolver um sistema para compartilhar recursos entre humanos não infectados nesse mundo.

## Documentação
> Para ver a documentação dessa API clique [aqui](https://documenter.getpostman.com/view/20514585/Uyr5nJiZ).

## Requerimentos
* asgiref==3.5.0
* Django==4.0.4
* django-filter==21.1
* djangorestframework==3.13.1
* Markdown==3.3.6
* psycopg2==2.9.3
* python-decouple==3.6
* pytz==2022.1
* sqlparse==0.4.2
* factory_boy==3.2.1
* Faker==13.3.4

##. env
* SECRET_KEY= Uma chave secreta do django que pode ser gerada [aqui](https://djecrety.ir/).
* DEBUG= True ou False
* DBUSER= O nome de usuario no banco de dados postgres
* DBPORT= O numero da porta no banco de dados postgres
* DBHOST= O nome do host no banco de dados postgres
* DBNAME= O nome do seu banco de dados postgres
* DBPASSWORD= A senha do seu banco de dados postgres

## Como executar
* certifque-se que o postgres está ativo
* no terminal, navegue para a pasta do projeto ```  ~/.../zssn/’  ```  
* execute no terminal ```  source venv/bin/activate```   para usar o ambiente virtual
* execute no terminal ```  python manage.py migrate```   para iniciar o servidor
* a ação acima deve mostrar o endereço a ser usado, como no exemplo abaixo:
>![Screenshot](https://i.imgur.com/633vvwx.png "Exemplo")

## Como testar
* Para testar o teste automatico execute o seguinte comando:
```  python manage.py test --keepdb ```  


