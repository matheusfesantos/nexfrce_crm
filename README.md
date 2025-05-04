# Sistema de Agendamento - Frappe Framework

Este repositório contém a implementação de um sistema de agendamento de compromissos utilizando o Frappe Framework, com integração ao MariaDB. A aplicação foi desenvolvida como parte do estudo de caso da Nexforce.

## Tecnologias Utilizadas
- **Frappe Framework** (Python e JavaScript)
- **MariaDB** (Banco de dados)
- **Git** (Versionamento de código)

## Funcionalidades
- Agendamento de compromissos com dados como:
  - Nome do Cliente
  - Data de Início e Fim
  - Duração
  - Descrição
  - Vendedor
  - Status do compromisso (Agendado, Finalizado, Cancelado)
- Validação para evitar que o vendedor tenha mais de um compromisso no mesmo horário.
- Visualização de compromissos em formato de calendário.

## Passos para Execução

### 1. **Configuração do Ambiente**
Para rodar o projeto, é necessário ter o **Frappe Bench** e o **MariaDB** instalados no seu ambiente local. Veja os passos abaixo para a instalação:

1. Instale o Frappe Bench:
   ```bash
   pip install frappe-bench
````

2. Instale o MariaDB no seu sistema. Para mais detalhes, consulte a [documentação do MariaDB](https://mariadb.org/).

3. Crie um banco de dados e um usuário no MariaDB, como descrito na documentação do Frappe.

4. Crie um novo site no Frappe Bench e configure o banco de dados MariaDB:

   ```bash
   bench new-site nome_do_site
   ```

### 2. **Problemas Encontrados e Soluções**

Durante o desenvolvimento do sistema de agendamento, encontrei diversos desafios e erros que precisei resolver para garantir que a aplicação funcionasse corretamente. Abaixo estão os principais problemas e suas soluções:

### **Erro 1: Falha na Conexão com o Banco de Dados MariaDB**

**Problema:**
O Frappe não conseguia se conectar ao banco de dados MariaDB. A mensagem de erro indicava que a conexão com o banco falhou, apesar de as credenciais estarem corretas. O Frappe tentava se conectar utilizando um `localhost`, mas o banco estava configurado para ouvir apenas em `127.0.0.1`.

**Solução:**
Verifiquei que o Frappe estava tentando se conectar com o banco de dados usando um hostname incorreto. No arquivo `sites/common_site_config.json`, alterei o campo `db_host` de `localhost` para `127.0.0.1` e reiniciei o servidor do Frappe:

```json
{
    "db_host": "127.0.0.1",
    "db_name": "frappe",
    "db_user": "frappe_user",
    "db_password": "sua_senha"
}
```

### **Erro 2: Conflito de Horários para o Vendedor**

**Problema:**
O sistema não estava verificando corretamente se o vendedor já tinha outro compromisso no mesmo horário. Isso causava a possibilidade de compromissos se sobreporem para o mesmo vendedor.

**Solução:**
Criei uma função de validação personalizada no Doctype "Appointment" para garantir que o vendedor não tenha compromissos sobrepostos. A consulta SQL foi ajustada para verificar se a data de início ou de término de um compromisso se sobrepõe a outro compromisso agendado para o mesmo vendedor. A validação ficou assim:

```python
@frappe.whitelist()
def validate(self):
    overlapping_appointments = frappe.db.sql("""
        SELECT name FROM `tabAppointment`
        WHERE seller = %s AND status = 'Scheduled'
        AND ((start_date <= %s AND end_date >= %s) OR (start_date <= %s AND end_date >= %s))
    """, (self.seller, self.start_date, self.start_date, self.end_date, self.end_date))

    if overlapping_appointments:
        frappe.throw("O vendedor já tem um compromisso neste horário.")
```

### **Erro 3: Problema com a Visualização de Calendário**

**Problema:**
O sistema não estava exibindo os compromissos no calendário, mesmo após a configuração do campo `start_date` e `end_date`. A visualização em calendário não estava sendo carregada corretamente.

**Solução:**
Ajustei o campo de visualização para garantir que os compromissos fossem exibidos corretamente no formato de calendário. Isso envolveu a configuração do campo para ser reconhecido pelo Frappe, e também modifiquei o script de inicialização do formulário para garantir que as datas de início e término fossem manipuladas corretamente. A alteração foi a seguinte:

```javascript
frappe.ui.form.on('Appointment', {
    onload: function(frm) {
        frm.fields_dict['appointments'].grid.get_field('start_date').get_datepicker().datepicker({ 
            minDate: new Date()
        });
    }
});
```

Além disso, ativei a visualização de calendário como a visualização padrão dentro da interface do Frappe.

### **Erro 4: Falha no Envio para o Repositório Git**

**Problema:**
Ao tentar enviar o código para o GitHub, percebi que o repositório não estava estruturado corretamente e faltava o arquivo `pyproject.toml`. Além disso, os arquivos estavam dispersos e não dentro do diretório `scheduling_system`.

**Solução:**
Criei o repositório no GitHub e garanti que a estrutura do repositório fosse correta. Organizei os arquivos dentro do diretório `scheduling_system`, adicionei o arquivo `pyproject.toml` na raiz do repositório e certifiquei-me de que o repositório incluísse apenas os arquivos necessários:

```bash
scheduling_system/
    ├── __init__.py
    ├── hooks.py
    ├── scheduling_system.py
    ├── pyproject.toml
```

### **Erro 5: Problema na Instalação do Frappe Bench**

**Problema:**
Durante a instalação do Frappe Bench, encontrei problemas relacionados a permissões e versões de dependências incompatíveis.

**Solução:**
Realizei a instalação do Frappe Bench em um ambiente virtual Python, o que garantiu que todas as dependências fossem isoladas e evitou conflitos de versões. Para criar o ambiente virtual, usei os seguintes comandos:

```bash
python3 -m venv frappe_env
source frappe_env/bin/activate
pip install frappe-bench
```

### **Erro 6: Erro ao Criar o Doctype "Appointment"**

**Problema:**
Após criar o Doctype "Appointment", os campos não estavam sendo corretamente salvos ou exibidos.

**Solução:**
Verifiquei que a definição do Doctype estava com tipos de campos errados, especialmente para `start_date` e `end_date`. Corrigi a definição dos campos para garantir que os tipos estivessem corretos (por exemplo, `Datetime` para `start_date` e `end_date`). A definição do Doctype ficou assim:

```python
class Appointment(Document):
    client_name = DataField()
    start_date = DatetimeField()
    end_date = DatetimeField()
    duration = TimeField()
    description = SmallTextField()
    seller = LinkField("User")
    status = SelectField(choices=["Scheduled", "Finished", "Canceled"])
```

### 3. **Instruções para Uso**

Após realizar os ajustes acima, a aplicação de agendamento está funcionando corretamente. Para rodar a aplicação, siga as instruções abaixo:

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/seu_usuario/scheduling_system.git
   cd scheduling_system
   ```

2. **Instale as dependências do Frappe:**

   ```bash
   bench update
   ```

3. **Inicie o servidor do Frappe:**

   ```bash
   bench start
   ```

4. Acesse a aplicação via navegador em `http://localhost:8000`.

## Conclusão

Este projeto ajudou a melhorar minhas habilidades com o Frappe Framework, especialmente na criação de Doctypes e na integração com o MariaDB. Ao longo do desenvolvimento, encontrei diversos erros e desafios, mas consegui resolvê-los com base na documentação do Frappe e na experiência adquirida.

Se você encontrar mais problemas ou precisar de ajuda, não hesite em abrir uma issue ou me contatar!

```

Com este `README.md`, você cobre todos os problemas encontrados e as soluções que foram aplicadas para resolvê-los. Ele fornece uma visão geral clara dos desafios enfrentados no processo de desenvolvimento e como cada um foi solucionado.
```