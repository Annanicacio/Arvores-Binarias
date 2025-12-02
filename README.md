Esse programa faz a inserção, remoção e busca de 100, 1000 e 10000 elementos e compara a eficiÊncia das operações em cada uma das estruturas de árvores. 
Os resultados são demonstrados no terminal por meio de uma tabela. O código foi feito em python.

teste

# 🏗️ Diagrama de Componentes

O diagrama abaixo ilustra a arquitetura do sistema de Biblioteca Pessoal, seguindo o padrão de camadas para separar a interface, as regras de negócio (como a validação de campos vazios) e o acesso aos dados.

```mermaid
componentDiagram
    direction TB

    package "Camada de Apresentação (Frontend)" {
        [Tela de Login/Logout] as UI_Auth
        [Lista de Livros & Paginação] as UI_List
        [Formulário de Livro] as UI_Form
        component "Cliente HTTP" as Client {
            [Gerenciador de Requisições]
        }
    }

    package "Camada de Negócio (Backend)" {
        portin "API REST (JSON)" as API_Port
        
        component "Controladores (Controllers)" as Controllers {
            [AuthController]
            [BookController]
        }
        
        component "Serviços (Services)" as Services {
            [AuthService]
            [BookService]
        }
        
        component "Persistência (Repositories)" as Repos {
            [UserRepository]
            [BookRepository]
        }
    }

    database "Banco de Dados" {
        [Tabela: Users]
        [Tabela: Books]
    }

    %% Relacionamentos
    UI_Auth ..> Client : Usa
    UI_List ..> Client : Usa ("Carregar Mais")
    UI_Form ..> Client : Usa (Salvar/Editar)

    Client --( API_Port : HTTPS / JSON
    API_Port -- Controllers

    Controllers --> Services : Solicita Lógica
    Services --> Repos : Solicita Dados

    Repos --> [Tabela: Users] : SQL/ORM
    Repos --> [Tabela: Books] : SQL/ORM

    %% Notas de Regras
    note right of [BookService]
        RN: Validação de Cadastro
        Impede salvar se todos os
        campos estiverem vazios.
    end note

    note left of [AuthService]
        RN: Segurança
        Login, Logout e Criptografia.
    end note

```mermaid
