import sqlite3
import pandas as pd


class ProductDBHelper:
    def __init__(self, name_db):
        self._name_db = name_db
        self.conn = None
        self.cursor = None
        self.connected = False

    def connect(self):
        self.conn = sqlite3.connect(self._name_db)
        self.cursor = self.conn.cursor()
        self.connected = True
        return self.cursor, self.connected

    def close(self):
        if self.conn:
            self.conn.close()
            self.connected = False


class TableProducts(ProductDBHelper):
    def __init__(self, name_db, name_table):
        super().__init__(name_db)
        self._name_table = name_table

    @property
    def name_db(self):
        return self._name_db
    @property
    def name_table(self):
        return self._name_table
    
    def create_table(self):
        try:
            query = f"""
                CREATE TABLE IF NOT EXISTS Produtos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    preco REAL NOT NULL
                );
            """
            db = ProductDBHelper("produtos.db")
            db.connect()
            db.cursor.execute(query)
            db.conn.commit()
            print(f"\nTabela {self.name_table} criado com sucesso.")
        except TypeError as e:
            print("Erro de tipagem ao criar a tabela", e)
        except AttributeError as e:
            print("Erro no Atributo ao criar a tabela", e)
    
    def insert(self, nome, preco):
        db = ProductDBHelper("produtos.db")
        db.connect()
        values_ = f"{nome}", f"{preco}"
        query = f"INSERT INTO {self.name_table} (nome, preco) VALUES (?,?)"
        try:
            db.cursor.execute(query, (values_))
            db.conn.commit()
            db.conn.close()
            print(f"Produto inserido no banco de dados.")
            return db.cursor.lastrowid
        except sqlite3.Error as e:
            print("Erro ao inserir os dados", e)
            return None
        
    def update(self, atribute, value, id):
        db = ProductDBHelper("produtos.db")
        db.connect()
        try:
            dados = f"{value}"
            query = f"UPDATE {self.name_table} SET {atribute} = ? WHERE id = ?"
            db.cursor.execute(query, (dados, id))
            db.conn.commit()
            db.conn.close()
            print(f"Produto de {id} foi alterado")
        except sqlite3.Error:
            print("\nTente novamente...")
            TableProducts.update(atribute=atribute, value=value, id=id)
    
    def view(self):
        db = ProductDBHelper("produtos.db")
        db.connect()
        try:
            query = "SELECT * FROM produtos"
            table_ = db.cursor.execute(query).fetchall()
            df = pd.DataFrame(table_)
            return df
        except sqlite3.OperationalError as e:
            print('Erro na Operação de Visualização do DB', e)
            return pd.DataFrame()
        finally:
            db.close()

    def delete(self, id):
        db = ProductDBHelper("produtos.db")
        db.connect()
        try:
            query = f"DELETE FROM {self.name_table} WHERE id = {id}"
            db.cursor.execute(query)
            db.conn.commit()
            db.conn.close()
        except sqlite3.Error:
            print("Erro ao tentar deletar ID Produto")


if __name__ == '__main__':
    produtos = TableProducts("produtos.db", "produtos")
    produtos.connect()
    produtos.view()
