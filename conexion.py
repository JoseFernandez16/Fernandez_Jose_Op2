import psycopg2
import pyttsx3

def insertar_datos(codigo_al,nombre_al,apellido_al,edad_al,nota1_al,nota2_al,nota3_al,promedio_al):
    sql= """INSERT INTO alumnos (codigo_al,nombre_al,apellido_al,edad_al,nota1_al,nota2_al,nota3_al,promedio_al) VALUES(%s,%s,%s,%s,%s,%s,%s,%s);"""
    conn =None
    try:
        conn = psycopg2.connect(
            host     = "localhost",
            database = "Examen_2",
            user     = "postgres",
            password = "fernandez22",
            port     = "5432")   
        cur=conn.cursor()
        cur.execute(sql,(codigo_al,nombre_al,apellido_al,edad_al,nota1_al,nota2_al,nota3_al,promedio_al))
        conn.commit()
        cur.close()
        if conn is not None:
            conn.close()
    except(Exception,psycopg2.DatabaseError)as e:
        print("Se encontró un error\n")
        print(e)
    finally:
        if conn is not None:
            conn.close()
        engine=pyttsx3.init()
        engine.say(f"El estudiante {nombre_al} fue registrado correctamente!!")
        engine.runAndWait()
    
def total_estudiantes():
    sql = """ SELECT * FROM alumnos;"""
    conn = None
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="Examen_2",
            user="postgres",
            password="fernandez22",
            port="5432")
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                
                if cur is not None:
                    fila = cur.fetchall()
                    return fila

        if conn is not None:
            conn.close()
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)
    finally:
        if conn is not None:
            conn.close()

def bus_estudiante(codigo_al):
    sql = """ SELECT nombre_al,apellido_al,nota1_al,nota2_al,nota3_al,promedio_al FROM alumnos WHERE codigo_al = %s ;"""
    conn = None
    cod=str(codigo_al)
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="Examen_2",
            user="postgres",
            password="fernandez22",
            port="5432")
            
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql,(cod,))
                
                if cur is not None:
                    row = cur.fetchall()
                    print(row)
                    return row

        if conn is not None:
            conn.close()
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)
    finally:
        if conn is not None:
            conn.close()
            
def editar_datos(nota1_al,nota2_al,nota3_al,promedio_al,codigo_al):
    sql= """UPDATE alumnos SET nota1_al=%s, nota2_al = %s, nota3_al = %s,promedio_al =%s WHERE codigo_al = %s;"""
    conn =None
    cod=str(codigo_al)
    no1=str(nota1_al)
    no2=str(nota2_al)
    no3=str(nota3_al)
    prom=str(promedio_al)
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="Examen_2",
            user="postgres",
            password="fernandez22",
            port="5432")
        cur=conn.cursor()
        cur.execute(sql,(no1,no2,no3,prom,cod))
        conn.commit()
        cur.close()
        if conn is not None:
            conn.close()
    except(Exception,psycopg2.DatabaseError)as e:
        print("Se encontró un error al actualizar \n")
        print(e)
    finally:
        engine=pyttsx3.init()
        engine.say("Los cambios fueron guardados exitosamente!!")
        engine.runAndWait()
        if conn is not None:
            conn.close()