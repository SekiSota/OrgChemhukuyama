import tkinter
from tkinter import BOTH, END, StringVar
import random
import csv
import datetime
import pandas as pd
import tkinter.ttk as ttk

root=tkinter.Tk()
root.title('福山本アプリ')
#define fonts and colors
root_color='#C1D37F'
input_color='#E2D58B'
output_color='#F9D4BB'
root.config(bg=root_color)

def hukuyama():
    n=random.randint(1,2)
    mondai_list=['A','B']#章の選択 いずれC問題を加え、A,B,Cから自由に選択できるようにしたい
    
    #問題番号の選出
    a=mondai_list[n-1]
    if a=='A':
        m=random.randint(1,78)
    elif a=='B':
        m=random.randint(1,128)
    b=a+str(m)
    text.set(b)
    #登場した問題の既出/初出判定
    df1=pd.read_csv('test.csv',index_col=0)#index_colを入れないとcsvファイルから読んだときにインデックスが追加され、形が合わない。
    list=df1['問題番号']
    B=b in list
    if B=='true':
        syosyutu_label=tkinter.Label(output_frame,text='既出です')
    else:
        syosyutu_label=tkinter.Label(output_frame,text='初です')
    syosyutu_label.grid(row=1, column=1)
    
def print_and_save():
    b=q_label["text"]
    if case_style.get()=='correct':
        d='正解'
    else:
        d='不正解'
    
    data={
        '問題番号':b,
        '正誤':d,
        '時間':datetime.datetime.now()
    }
    df1=pd.read_csv('test.csv',index_col=0)
    df2=pd.DataFrame([data])
    df3=pd.concat([df1, df2], axis=0)
    df3.to_csv('test.csv')
          

def check():
    df=pd.read_csv('test.csv')
    root_df=tkinter.Tk()
    tree = ttk.Treeview(root_df)
    tree["columns"] = (1,2,3)
    tree["show"] = "headings"
    tree.column(1)
    tree.column(2)
    tree.column(3)
    tree.heading(1,text='問題番号')
    tree.heading(2,text="正誤")
    tree.heading(3,text="時間")
    for i in range(len(df['問題番号'])) :
        tree.insert("","end",values=(df['問題番号'][i],df['正誤'][i],df['時間'][i]))
    tree.pack(anchor='center')
    root_df.mainloop()

def switchButtonState():
    if (submit_button['state'] == tkinter.NORMAL):
        submit_button['state'] = tkinter.DISABLED
    else:
        submit_button['state'] = tkinter.NORMAL
#define layout
#deine frame
input_frame=tkinter.LabelFrame(root, bg=input_color)
output_frame=tkinter.LabelFrame(root, bg=output_color)
input_frame.grid(row=0,column=0)
output_frame.grid(row=0, column=1, pady=(0,10) )
text=tkinter.StringVar()
text.set('問題番号')
q_label=tkinter.Label(output_frame, textvariable=text)
syosyutu_label=tkinter.Label(output_frame)
syosyutu_label.grid(row=1, column=1,sticky='we')
q_label.grid(row=1,column=0,sticky='we')

#radiobutton
case_style=StringVar()
case_style.set('correct')
correct_button=tkinter.Radiobutton(output_frame, text='正解', variable=case_style, value='correct', bg=input_color)
false_button=tkinter.Radiobutton(output_frame, text='不正解', variable=case_style, value='false', bg=input_color)
correct_button.grid(row=0, column=0, padx=2, pady=2)
false_button.grid(row=0, column=1, padx=2, pady=2)


#create widget
randam=tkinter.Button(input_frame, text='問題選出', command=lambda:[hukuyama(),switchButtonState()])
randam.pack(padx=10,pady=(10,10))

submit_button=tkinter.Button(output_frame, text='提出', command=lambda:[print_and_save(),switchButtonState()], state=tkinter.DISABLED)
submit_button.grid(row=1, column=2, padx=2, pady=2)

result=tkinter.Button(output_frame, text='履歴確認', command=check)
result.grid(row=2,column=0)


root.mainloop()