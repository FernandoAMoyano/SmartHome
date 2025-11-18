"""Implementación DAO para la entidad User."""

from typing import List, Optional
from mysql.connector import Error
from interfaces.i_user_dao import IUserDao
from dominio.user import User
from conn.db_connection import DatabaseConnection
from dao.role_dao import RoleDAO


class UserDAO(IUserDao):
    """Data Access Object para gestionar usuarios."""
    
    def __init__(self):
        """Inicializa el DAO con la conexión a BD."""
        self.db = DatabaseConnection()
        self.role_dao = RoleDAO()
    
    def insertar(self, entidad: User) -> bool:
        """Inserta un nuevo usuario."""
        try:
            cursor = self.db.get_cursor()
            query = """
                INSERT INTO user (email, password, name, role_id) 
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (
                entidad.email,
                entidad.password,
                entidad.name,
                entidad.role.id
            ))
            self.db.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Error al insertar usuario: {e}")
            self.db.rollback()
            return False
    
    def modificar(self, entidad: User) -> bool:
        """Modifica un usuario existente."""
        try:
            cursor = self.db.get_cursor()
            query = """
                UPDATE user 
                SET password = %s, name = %s, role_id = %s 
                WHERE email = %s
            """
            cursor.execute(query, (
                entidad.password,
                entidad.name,
                entidad.role.id,
                entidad.email
            ))
            self.db.commit()
            affected = cursor.rowcount > 0
            cursor.close()
            return affected
        except Error as e:
            print(f"Error al modificar usuario: {e}")
            self.db.rollback()
            return False
    
    def eliminar(self, email: str) -> bool:
        """Elimina un usuario por email."""
        try:
            cursor = self.db.get_cursor()
            query = "DELETE FROM user WHERE email = %s"
            cursor.execute(query, (email,))
            self.db.commit()
            affected = cursor.rowcount > 0
            cursor.close()
            return affected
        except Error as e:
            print(f"Error al eliminar usuario: {e}")
            self.db.rollback()
            return False
    
    def obtener_por_id(self, email: str) -> Optional[User]:
        """Obtiene un usuario por email (ID en este caso)."""
        return self.obtener_por_email(email)
    
    def obtener_por_email(self, email: str) -> Optional[User]:
        """Obtiene un usuario por su email."""
        try:
            cursor = self.db.get_cursor()
            query = """
                SELECT email, password, name, role_id 
                FROM user 
                WHERE email = %s
            """
            cursor.execute(query, (email,))
            row = cursor.fetchone()
            cursor.close()
            
            if row:
                role = self.role_dao.obtener_por_id(row['role_id'])
                if role:
                    return User(
                        row['email'],
                        row['password'],
                        row['name'],
                        role
                    )
            return None
        except Error as e:
            print(f"Error al obtener usuario: {e}")
            return None
    
    def obtener_todos(self) -> List[User]:
        """Obtiene todos los usuarios."""
        try:
            cursor = self.db.get_cursor()
            query = "SELECT email, password, name, role_id FROM user"
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            
            usuarios = []
            for row in rows:
                role = self.role_dao.obtener_por_id(row['role_id'])
                if role:
                    usuarios.append(User(
                        row['email'],
                        row['password'],
                        row['name'],
                        role
                    ))
            return usuarios
        except Error as e:
            print(f"Error al obtener usuarios: {e}")
            return []
    
    def cambiar_rol(self, email: str, nuevo_rol_id: int) -> bool:
        """Cambia el rol de un usuario."""
        try:
            cursor = self.db.get_cursor()
            query = "UPDATE user SET role_id = %s WHERE email = %s"
            cursor.execute(query, (nuevo_rol_id, email))
            self.db.commit()
            affected = cursor.rowcount > 0
            cursor.close()
            return affected
        except Error as e:
            print(f"Error al cambiar rol: {e}")
            self.db.rollback()
            return False
    
    def validar_credenciales(self, email: str, password: str) -> Optional[User]:
        """Valida las credenciales de un usuario."""
        user = self.obtener_por_email(email)
        if user and user.validate_credentials(email, password):
            return user
        return None