# Alumnos
# Buenrostro Puerta Delfina Montserrat
# Guzmán Reyes Bryan Sean
# Montoya Figueroa Josué Eduardo

import tkinter as tk
import sympy as sp 
import numpy as np
import sys
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from idlelib.tooltip import Hovertip
import tkinter.messagebox as messagebox
from sympy.plotting import plot
from scipy.integrate import odeint
#
#
# NOTA: Es importante que instalen la libreria tkinter: "pip install tk" o "pip install tkinter"
#
#

ecu = None
soluG = None
x, y = sp.symbols('x y')
y = sp.Function('y')

def center_window(window, width, height):
    # Calcula las coordenadas para centrar la ventana en la pantalla
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    xW = (screen_width // 2) - (width // 2)
    yH = (screen_height // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{xW}+{yH}')

def create_interface():
    # Funciones para abrir nuevas interfaces
    
    def mostrar_solucion_particular():
        particular_window = tk.Toplevel(root)
        particular_window.title("Solución Particular")
        center_window(particular_window, 600, 600)

        def graficar():
            global ecu
            global soluG
            x = sp.symbols('x')
            y = sp.Function('y')(x)
            C1 = sp.Symbol('C1')

            y0 = float(entry_y.get())
            x0 = float(entry_x.get())

            # Obtener solución particular
            solu1 = sp.dsolve(ecu, y, ics={y.subs(x, x0): y0})
            # Obtener valor de C
            sol_with_C1 = soluG.subs('C1', C1)
            # Resuelve para C1 usando los valores dados para x e y
            eq_C1 = sp.Eq(sol_with_C1.rhs.subs(x, x0), y0)
            C1_value = float(sp.solve(eq_C1, C1)[0])
            # Valores de y para la grafica
            y_sol = sp.lambdify(x, solu1.rhs, 'numpy')
            # Genera los datos para la gráfica
            x_vals = np.linspace(x0, x0+20, 100)
            y_vals = y_sol(x_vals)
            # Crea la gráfica
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.plot(x_vals, y_vals, label=(str(ecu) + "\ny(" + str(x0) + ")" + "=" + str(y0) + "\nC= " + str(C1_value)))
            #ax.plot(x_vals, y_vals, label=ecuText)
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.legend()
            ax.grid(True)

            # Limpia el canvas anterior antes de dibujar el nuevo
            for widget in frame_plot.winfo_children():
                widget.destroy()

            canvas = FigureCanvasTkAgg(fig, master=frame_plot)
            canvas.draw()
            canvas.get_tk_widget().pack()
            
        def verificar_entrada():
            valorX = entry_x.get()
            valorY = entry_y.get()
            if valorX and valorX:  # Verificar si las entradas no están vacías
                try:
                    # Intentar los valores a flotante para verificar que sean numeros
                    float(valorX)  
                    float(valorY)
                    graficar() # Manda llamar a la función mostrar_solucion_particular() para graficar la solución particular
                except ValueError:
                    messagebox.showerror("Error", "Ingrese un número válido.")
            else:
                messagebox.showwarning("Advertencia", "El campo está vacío.")

        frame1 = tk.Frame(particular_window)
        frame1.pack(pady=10)

           # Botones para mostrar las soluciones particular, general e isoclinas
        label_valores = tk.Label(frame1, text="Ingrese los valores de x e y", font=("Helvetica", 12))
        label_valores.pack(side=tk.TOP)

        label_x0 = tk.Label(frame1, text="y (")
        label_x0.pack(side=tk.LEFT)

        entry_y = tk.Entry(frame1, font=("Helvetica", 12), width=10)
        entry_y.insert(tk.END, "")
        entry_y.pack(side=tk.LEFT)

        label_y0 = tk.Label(frame1, text=") = ")
        label_y0.pack(side=tk.LEFT)

        entry_x = tk.Entry(frame1, font=("Helvetica", 12), width=10)
        entry_x.insert(tk.END, "")
        entry_x.pack(side=tk.LEFT)

        btn_plot = tk.Button(particular_window, text="Graficar", command=verificar_entrada)
        btn_plot.pack(side=tk.TOP)       
        
        frame_plot = tk.Frame(particular_window)
        frame_plot.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)            
        
    def mostrar_solucion_general():
        general_window = tk.Toplevel(root)
        general_window.title("Familia de curvas")
        center_window(general_window, 600, 600)
        # Aquí puedes agregar el contenido de la interfaz para la solución general

        def graficar():
            global ecu
            global soluG

            curvas = int(entry_curvas.get())

            x = sp.symbols('x')
            y = sp.Function('y')(x)
            C1 = sp.Symbol('C1')

            # Genera los datos para la gráfica
            x_vals = np.linspace(-15, 30, 100)

            # Crea la gráfica
            fig, ax = plt.subplots(figsize=(8, 6))
            
            # Itera sobre diferentes valores de la constante C1
            C1_values = np.linspace(-10, 10, curvas)
            for C1_value in C1_values:
                solu_with_C1 = soluG.subs('C1', C1_value)
                y_sol = sp.lambdify(x, solu_with_C1.rhs, 'numpy')
                y_vals = y_sol(x_vals)
                ax.plot(x_vals, y_vals, label=f'C1={C1_value:.2f}')

            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.legend()
            ax.grid(True)

            # Limpia el canvas anterior antes de dibujar el nuevo
            for widget in frame_plot.winfo_children():
                widget.destroy()

            canvas = FigureCanvasTkAgg(fig, master=frame_plot)
            canvas.draw()
            canvas.get_tk_widget().pack()
            
        def verificar_entrada():
            curvas = entry_curvas.get()
            if curvas: # Verificar si las entradas no están vacías
                try:
                    # Intentar los valores a flotante para verificar que sean numeros
                    float(curvas)  
                    graficar() # Manda llamar a la función mostrar_solucion_particular() para graficar la solución particular
                except ValueError:
                    messagebox.showerror("Error", "Ingrese un número válido.")
            else:
                messagebox.showwarning("Advertencia", "El campo está vacío.")

        frame1 = tk.Frame(general_window)
        frame1.pack(pady=10)

           # Botones para mostrar las soluciones particular, general e isoclinas
        label_curvas = tk.Label(frame1, text="Ingrese la cantidad de curvas a visualizar", font=("Helvetica", 12))
        label_curvas.pack(side=tk.LEFT)

        entry_curvas = tk.Entry(frame1, font=("Helvetica", 12), width=10)
        entry_curvas.insert(tk.END, "10")
        entry_curvas.pack(side=tk.LEFT)

        btn_plot = tk.Button(general_window, text="Graficar", command=verificar_entrada)
        btn_plot.pack(side=tk.TOP)       
        
        frame_plot = tk.Frame(general_window)
        frame_plot.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)  

    def mostrar_isoclinas():
        '''particular_window = tk.Toplevel(root)
        particular_window.title("Solución Particular")
        center_window(particular_window, 600, 600)'''
        # Aquí puedes agregar el contenido de la interfaz para las isoclinas
        global ecu
        # Tomar el lado derecho de la ecuación
        rhsCadena = str(ecu.rhs)
        # Reemplazar y(x) por y
        rhsCadena = rhsCadena.replace("y(x)","y")
        expr = sp.sympify(rhsCadena)  
        ed = sp.lambdify((x, y), expr, 'numpy')

        # Función para graficar las isoclinas
        def isoclinas(f, x_range, y_range, c_vals):
            X, Y = np.meshgrid(x_range, y_range)
            plt.figure(figsize=(800/96, 600/96), dpi=96)
            for c in c_vals:
                Z = f(X, Y) - c
                plt.contour(X, Y, Z, levels=[0], colors='blue', linestyles='dotted')

            # Función para dibujar el campo de direcciones
        def campo_direcciones(f, x_range, y_range, step=1):
            X, Y = np.meshgrid(np.arange(x_range[0], x_range[1], step),
                            np.arange(y_range[0], y_range[1], step))
            U = 1
            V = f(X, Y)
            N = np.sqrt(U**2 + V**2)
            U2, V2 = U/N, V/N
            plt.quiver(X, Y, U2, V2, angles='xy')
        
        # Función para resolver y graficar la solución de la ecuación
        def resolver(f, x0, y0, x_range):
            x = np.linspace(x_range[0], x_range[1], 100)
            sol = np.zeros_like(x)
            sol[0] = y0
            for i in range(1, len(x)):
                sol[i] = sol[i - 1] + f(x[i - 1], sol[i - 1]) * (x[i] - x[i - 1])
            plt.plot(x, sol, label=f'Condición inicial: ({x0},{y0})')

        # Definir los rangos y valores
        x_range = (-10, 10)
        y_range = (-10, 10)
        c_values = np.linspace(-10, 10, 20)

        # Graficar las isoclinas, el campo de direcciones y la solución de la ODE
        isoclinas(ed, np.linspace(x_range[0], x_range[1], 100), np.linspace(y_range[0], y_range[1], 100), c_values)
        campo_direcciones(ed, x_range, y_range)
        resolver(ed, 0, 0, x_range)

        # Limpiar la figura antes de cada nueva gráfica
        
        plt.title(f'y\' = {str(ecu)}')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.legend()
        plt.show()   
        plt.clf()

        
    
    def generar_solucion_general():
        try:
            fun = ecuacion_entry.get()

            # Se remplaza la cadena leida para transformarla en una función leíble por el programa
            fun = fun.replace("y","y(x)")
            fun = fun.replace("y(x)'","y(x).diff()")
            fun = fun.replace("y(x).diff()'","y(x).diff(x,2)")
            fun = fun.replace("y(x).diff(x,2)'","y(x).diff(x,3)")
            fun = fun.replace("y(x).diff(x,3)'","y(x).diff(x,4)")
            fun = fun.replace("sen","sin")
            fun = fun.replace("sin","sp.sin")
            fun = fun.replace("cos","sp.cos")
            fun = fun.replace("tan","sp.tan")
            fun = fun.replace("sec","sp.sec")
            fun = fun.replace("csc","sp.csc")
            fun = fun.replace("ctg","sp.ctg")
            fun = fun.replace("e^","sp.exp")
            fun = fun.replace("ln","sp.ln")
            fun = fun.replace("^","**")
            fun = fun.replace("sqrt", "sp.sqrt")

            # Se separan las 2 partes de la ecuación
            fun1 = fun.split("=")[0]
            fun2 = fun.split("=")[1]
            #   Convertir string en SymPy
            lhs = sp.parse_expr(fun1, transformations='all', local_dict={'y': y, 'x': x})
            rhs = sp.parse_expr(fun2, transformations='all', local_dict={'y': y, 'x': x, 'sp': sp})

            # Construir ecuación
            global ecu
            ecu = sp.Eq(lhs, rhs)
            
            if primer_orden(): # Manda llamar a la función primer_orden() para verificar que la ecución sea de primer orden
                if explicita(): # Mnada llamar a la función explicita() para convertir función a explicita encaso de que sea implicita
                    #if simbolos():
                    if homogenea(ecu.rhs): # Manda llamar a la función homogenea para verificar que la ecuación ingresada sea homogenea
                        global soluG 
                        soluG= sp.dsolve(ecu)
                        solu = str(soluG)
                        # Se remplaza la solución dada para transformarla en una función leíble por el usuario
                        solu = solu[3:-1]
                        solu = solu.replace("**","^")
                        solu = solu.replace("y(x)","y")
                        solu = solu.replace(", "," = ")
                        solu = solu.replace("exp","e^")
                        # Se manda a llamar a la función sentMesaje() para que muentre la solución al usuario
                        sentMensaje(solu, True)
                        
                    else:
                        sentMensaje("Error: La ecuación ingresada no es homogénea, intente otro método", False)
                        return
                    #else:
                        #sentMensaje("Error: solo se acepan los símbolos x e y(x)", False)
                else:
                    sentMensaje("Error en la sintaxis de la ecuación", False)
                    return
            else: 
                sentMensaje("Error: la ecuación ingresada no es de primer orden", False)
                return

                               
        except ValueError:
            sentMensaje("Error: La ecuación diferencial ingresada no es válida", False)
            return
        except IndexError:
            sentMensaje("Error: La ecuación diferencial ingresada no es válida", False)
            return
        except ZeroDivisionError:
            sentMensaje("No se puede dividir por cero.", False)
            return
        except:            
            error_type = sys.exc_info()[0]
            sentMensaje("Error: " + str(error_type), False)
            return
    
    def simbolos():
        # Definir las variables
        x = sp.symbols('x')
        y = sp.Function('y')(x)

        global ecu
        # Obtener los símbolos libres de la ecuación
        free_symbols = ecu.free_symbols
        # Obtener las funciones dependientes de x
        dependiente = {f for f in ecu.atoms(sp.Function) if f.args == (x,)}

        # Definir el conjunto de símbolos permitidos
        simbolos = {x}
        funciones = {y}

        # Comprobar si los símbolos libres son solo x y y(x)
        if free_symbols == simbolos and dependiente == funciones: return True
        else: return False
        
    # Función para comprobar que la ecuación sea de primer grado
    def primer_orden():
        global ecu
        # Crear símbolo para la variable independiente (x) y la función dependiente (y)
        x = sp.symbols('x')
        y = sp.Function('y')(x)
        
        # Obtener todas las derivadas en la ecuación
        derivadas = ecu.atoms(sp.Derivative)
        
        # Verificar si todas las derivadas son de primer orden
        for deriv in derivadas:
            if deriv.derivative_count != 1 or deriv.args[0] != y:
                return False # Si hay más de una derivada devuelve false
        return True

    # Función para despejar y' y que la función sea explicita
    def explicita():
        global ecu
        # Definir la variable y la función dependiente
        x = sp.Symbol('x')
        y = sp.Function('y')(x)

        try:
            # Resolver la ecuación para la derivada de y respecto a x
            sol = sp.solve(ecu, y.diff(x))
            # Mostrar el resultado en la forma explicita
            ecuExplicita = sp.Eq(y.diff(x), sol[0])
            ecu = ecuExplicita
            return True
        except:
            return False
        

    # Funcion para validar que la ED sea homogénea
    def homogenea(rhs):
        # Definir las variables
        x, y, t = sp.symbols('x y t')
        #fun2 = (y-x) / x
        rhsCadena = str(rhs)
        rhsCadena = rhsCadena.replace("y(x)","y")
        rhs = sp.sympify(rhsCadena)

        # Sustituir x = tx y y = ty en la ecuación
        substituted_eq = rhs.subs([(x, t*x), (y, t*y)])

        # Simplificar la ecuación sustituida
        simplified_eq = sp.simplify(substituted_eq)

        # Verificar si se puede eliminar t de la ecuación simplificada
        if simplified_eq.as_expr().has(t): return False
        else: return True
               
    def sentMensaje(mensaje, btn):
        respuesta_text.config(state="normal")
        respuesta_text.delete("1.0", tk.END)
        respuesta_text.insert("1.0", mensaje)
        respuesta_text.config(state="disabled")             
        
        if btn: btnEnable()
        else: btnDisable()

    def btnDisable():
        particular_button.config(state=tk.DISABLED)
        general_button.config(state=tk.DISABLED)
        isoclina_button.config(state=tk.DISABLED)
    
    def btnEnable():
        particular_button.config(state=tk.NORMAL)
        general_button.config(state=tk.NORMAL)
        isoclina_button.config(state=tk.NORMAL)
    
    # Fución para finalizar el programa
    def on_closing():
        root.destroy()
        root.quit()  
    
    # Función para mpostrar cuadro de dialogo con la sintaxis que debe tener la ED
    def show_dialog():
        messagebox.showinfo("Términos aceptados", "y\n x\n y'\n y''\n y'''\n sen/sin\n cos\n tan\n sec\n csc\n ctg\n e^\n ln\n Ejemplos:\n multiplicar: xy*3\n dividir: ((x^3)-(y^4))/(2*x*y)\n raiz: sqrt((x^2)+(y^2))")

    # Crear la ventana principal
    root = tk.Tk()
    root.title("Sistema de solucion de ecuaciones diferenciales")
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Centrar la ventana en la pantalla
    center_window(root, 600, 400)
    
    # Agregar un título
    title_label = tk.Label(root, text="Homogéneas Ordinarias", font=("Helvetica", 16))
    title_label.pack(pady=20)
    
    frame1 = tk.Frame(root)
    frame1.pack(pady=10)
    frame2 = tk.Frame(root)
    frame2.pack(pady=10)
    frame3 = tk.Frame(root)
    frame3.pack(pady=10)
    # Campo de texto para mostrar una ecuación diferencial de ejemplo
    ecuacion_entry = tk.Entry(frame1,  font=("Helvetica", 12), width=50)
    ecuacion_entry.pack(side=tk.LEFT)

    btnTool = tk.Button(frame1, text="?", command=show_dialog)
    btnTool.pack(side=tk.LEFT)
    mensaje = Hovertip(btnTool, "Términos aceptados")

    generar_general_botton = tk.Button(frame2, text="Generar solución", command=generar_solucion_general)
    generar_general_botton.pack(side="top")

    # Campo de texto para la respuesta    
    respuesta_text = tk.Text(frame2, wrap="word", state='disabled', font=("Helvetica", 12), height=2, width=50)
    respuesta_text.insert(tk.END, "")
    respuesta_text.pack(expand=True)
    
    # Botones para mostrar las graficas
    particular_button = tk.Button(root, text="Mostrar gráfica de la solución particular", command=mostrar_solucion_particular,state=tk.DISABLED)
    particular_button.pack(side=tk.TOP)
    
    general_button = tk.Button(root, text="Mostrar familia de curvas", command=mostrar_solucion_general, state=tk.DISABLED)
    general_button.pack(side="top", padx=20, pady=10)
    
    #isoclina_button = tk.Button(root, text="Mostrar isoclinas", command=mostrar_isoclinas, state=tk.DISABLED)
    isoclina_button = tk.Button(root, text="Mostrar isoclinas", command=mostrar_isoclinas,state=tk.DISABLED)
    isoclina_button.pack(side="top", padx=20, pady=10)
    

    # Ejecutar el bucle principal de la aplicación
    root.mainloop()

# Llamar a la función para crear la interfaz
create_interface()