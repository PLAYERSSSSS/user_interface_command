# user interface command

### 一个用于开发跨平台的命令行用户界面的库

## [zh_CN]
> 通过 Frame类来实列化一个命令行界面对象  
> 通过Frame对象中的 addWidget(self, widget, row: int, column: int)成员函数插入小组件  
> 注: widget 为小组件对象 row指定插入第几行(从0开始) column指定插入第几列(从0开始)  
> 完成所有小组件对象的插入后调用 Frame对象中的 reset()成员函数刷新命令行  

## [en_US]
> Instantiate a command line interface object using the Frame class.  
> Insert the widget through the addWidget(self, widget, row: int, column: int) member function in the Frame object.  
> Note: widget specifies which row to insert (starting from 0) column specifies which column to insert (starting from 0).  
> After all widget objects have been inserted, the reset() member function in the Frame object is called to refresh the command line.  

## Demo 示范
```Python
from UIC import Frame
from UIC.module.Button import Button
from UIC.module.Label import Label

w = Frame(5, 5)

button = Button("text")
button.setHoveBackColor((255, 255, 255))
button.setHoveColor((0, 0, 0))
label = Label("text")

w.addWidget(button, 0, 0)
w.addWidget(label, 0, 1)
w.addWidget(button, 0, 2)
w.reset()
```
