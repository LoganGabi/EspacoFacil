<h1>EspacoFacil</h1>

</h3>O "Espaço Fácil" é um software que visa o cadastro e os agendamentos de espaços, tornando o processo de gerenciar e solicitar uma sala mais fácil, rápido e seguro.</h3>

<b>Desgin figma:</b> https://www.figma.com/design/lrlSXj7DE2oQmMoQBYDuye/Espaco-Facil?node-id=5-3&t=DZ7F5VsrxsusPGxz-1

<b>Documento de Requisitos:</b> https://docs.google.com/document/d/17a0FGlAt899scT_it9LaTSinnnT-zXBRiINy1despq8/edit?tab=t.0
<h3>🧑‍💻 Como rodar o projeto</h3>
<b>Clonar o projeto:</b>

> git clone <link-do-seu-repositório-ou-compartilhamento></br> 
> cd espacofacil_api

<b>Instalar o Docker:</b></br> 
https://www.docker.com/products/docker-desktop

<b>Criar arquivo .env</b></br>
> path: espacofacil_api/espacofacil_api </br>
> *"utilize o arquivo espacofacil_api/espacofacil_api/.env_example como base para preencher"*

<b>Subir o projeto:</b></br> 
> cd espacofacil_api </br>
> docker-compose up --build </br>

-- "Abra um novo terminal" </br>
> cd espacofacil_api </br>
> docker ps </br>

-- "Busque o campo < NAMES > ou < CONTAINER ID > do container. E execute-o com o codigo abaixo" </br>
> docker exec -it < NAMES ou CONTAINER ID > /bin/bash </br>

-- "Caso o acima de erro tente o abaixo" </br>
> docker exec -it < NAMES ou CONTAINER ID > /sh </br>

-- "Por fim execulte as migrates" </br>
> python manage.py makemigrations </br>
> python manage.py migrate </br>

-- "!! Toda edição nas models.py deve ser concluida com os comandos migrates" </br>

<b>Acessar no navegador:</b></br> 
http://localhost:8000

-- "Ao finalizar toda configuração pela primeira vez, somente o docker-compose up ja inicializa o projeto"
