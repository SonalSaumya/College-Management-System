from tkinter import*
import mysql.connector
from tkinter import ttk
root =Tk()
root.title("Notice Board")
root.geometry("900x500+200+100")
root.resizable(False, False) 
global root_window
root_window = root
def on_closing():
    root_window.destroy()
def search():
    option = dropdown.get()
    search_input = searchInput.get()
    db = mysql.connector.connect(host="localhost", user="root", password="", database="nsec_db")
    mycursor = db.cursor()
    if search_input == "":
        mycursor.execute("SELECT * FROM notice_board")
    elif option == "UID":
        mycursor.execute("SELECT * FROM notice_board WHERE id = '" + str(search_input) + "'")
    elif option == "Topic":
        mycursor.execute("SELECT * FROM notice_board WHERE topic = '" + str(search_input).upper() + "'")
    else:
        return
    rows = mycursor.fetchall()
    data_table.delete(*data_table.get_children())
    if rows == None:
        note_text['text'] = "Data: 0 Rows"
        return 
    note_text['text'] = "Data: "+str(len(rows))+" Rows"
    for row in rows:
        data_table.insert('', END, values=row)
    db.commit()
    db.close()
    # pass

# IT WILL GET DATA IN LEFTBOX (getdata made events there and fecth value there also)
def getdata(event):
    currow = data_table.focus()
    contents = data_table.item(currow)
    row = contents['values']
    IdEntry.configure(state='normal')
    TopicEntry.configure(state='normal')
    DescriptionEntry.configure(state='normal')
    IdEntry.delete(0, END)
    TopicEntry.delete(0, END)
    DescriptionEntry.delete("1.0", "end")
    IdEntry.insert(0, row[0])
    IdEntry.configure(state='readonly')
    TopicEntry.insert(0, row[1])
    DescriptionEntry.insert(END, row[2])
    TopicEntry.configure(state='readonly')
    DescriptionEntry.configure(state='disabled')

#Header
header=Frame(root, bg="brown", bd=0)
header.place(x=0,y=0,width=900,height=75)

#heading label
nsec=Label(header, text="Birsa Institute of Technology",font=("Helvetica", 28,"bold"), bg = "brown",fg="#eae2b7")
nsec.place(x=0, y=10, width=900)
#Profile frame
frame2=Frame(root, bg="#fbb1bd")
frame2.place(x=0,y=75,width=900,height=50)
welcome_text = Label(frame2, text = "Search Notice Board", font=("Minion Pro Regular", 16), bg="#fbb1bd")
welcome_text.place(x=20, y=10)
close = Button(frame2, text = "Close", command = on_closing, bd = 0, font=("Minion Pro Regular", 16), bg="#fff", fg = "#000")
close.place(x=830, y=0, height = 50, width = 70)
# LEFT BOX
leftbox=Frame(root,bd=0,bg="brown")
leftbox.place(x=10,y=140,width=500,height=350)

# INSIDE LEFT BOX
leftbox_title=Label(leftbox,text="View Details",font=("Helvetica",20,"bold"),fg="#eae2b7",bg="brown")
leftbox_title.place(x=10, y=10, width=  500)
IdLabel=Label(leftbox,text="ID",font=("Helvetica",15),fg="#eae2b7",bg="brown")
IdLabel.place(x=10, y =50)
IdEntry=Entry(leftbox,font=("Helvetica",15),bd=0)
IdEntry.configure(state='readonly')
IdEntry.place(x=50, y =50, width = 80)
TopicLabel=Label(leftbox,text="Topic",font=("Helvetica", 15),fg="#eae2b7",bg="brown")
TopicLabel.place(x=200, y=50)
TopicEntry=Entry(leftbox,font=("Helvetica", 15),bd=0)
TopicEntry.configure(state='readonly')
TopicEntry.place(x=270, y=50, width = 200)
DescriptionLabel=Label(leftbox,text="Description",font=("Helvetica", 15),fg="#eae2b7",bg="brown")
DescriptionLabel.place(x=10, y=80)
scrolly=Scrollbar(leftbox,orient=VERTICAL)
DescriptionEntry=Text(leftbox, font=("Helvetica", 15),bd=0, yscrollcommand=scrolly.set)
DescriptionEntry.insert(END, "Select Notice to view details")
DescriptionEntry.configure(state='disabled')
scrolly.config(command=DescriptionEntry.yview)
DescriptionEntry.place(x=10, y=110, width = 450, height = 200)
scrolly.place(x=460, y=110, height = 200)

# RIGHT BOX
rightbox=Frame(root,bd=0,bg="indianred")
rightbox.place(x=500,y=140,width=390,height=350)

# RIGHT BOX HEADING
searchInput=Entry(rightbox,font=("Helvetica", 12),bd=0,width=17)
searchInput.place(x=10, y=10, height = 30)
dropdown=ttk.Combobox(rightbox,font=("Helvetica",10),state='readonly', width = 10)
dropdown['values']=("--Search By--", "UID", "Topic")
dropdown.current(0)
dropdown.place(x=180, y=10, height = 30)
searchBtn=Button(rightbox,text="Search",command=search,font=("Helvetica", 12),width=10, bd = 0)
searchBtn.place(x=280, y=10, height = 30)

# BOX INSIDE RIGHT BOX
tabfrm=Frame(rightbox,bd=4,relief=RIDGE,bg="lightblue")
tabfrm.place(x=10,y=50,width=370,height=270)
scrolly=Scrollbar(tabfrm,orient=VERTICAL)
data_table=ttk.Treeview(tabfrm,columns=("id","name","description"),yscrollcommand=scrolly.set)
scrolly.pack(side=RIGHT,fill=Y)
scrolly.config(command=data_table.yview)

note_text=Label(rightbox,font=("Helvetica", 10),bg="indianred",fg="white")
note_text.place(x=10, y=325)

# INSIDE RIGHT BOX
data_table.heading("id",text="ID")
data_table.heading("name",text="Topic")
data_table.heading("description",text="Description")
data_table['show']="headings"
data_table.column("id",width = 10)
data_table.column("name",width=50)
data_table.column("description",width=30)
data_table.pack(fill=BOTH,expand=1)
data_table.bind("<ButtonRelease-1>",getdata)

search()

root.mainloop()