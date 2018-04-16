# -*- coding: UTF-8 -*- 
#--------------------------------------------------------------------------
#
# ScriptName : Normal Translator Beta1.0
# Contents   : Normal editing
# Author	 : Yiyang Chen
# Update	 : 2017/7/8
# Note	   : Credits to Charlie McKenna for helping me out
#			   
#--------------------------------------------------------------------------
##########Read me

##中文在下面

First of all, thank you for your support and trying out this tool. This tool is my first attempt to create something python based in maya. 
If there is any bugs or problems, please do not hesitate to complain towards this email: yiyangchen@gmail.com

In order to set up the tool please:
1. Put the files in a custom dictionary; recommended to put in folder '/Users/Documents/maya/2017/scripts/YiyangTools/'
2. Please copy and paste the following !!!Python!!! script to the script editor, or the shelf editor command and run:
"

import sys
import os
 
def psource(module):

    file = os.path.basename( module )
    dir = os.path.dirname( module )

    toks = file.split( '.' )
    modname = toks[0]


    if( os.path.exists( dir ) ):
        paths = sys.path
        pathfound = 0
        for path in paths:
            if(dir == path):
                pathfound = 1

        if not pathfound:
            sys.path.append( dir )

    exec ('import ' + modname) in globals()

    exec( 'reload( ' + modname + ' )' ) in globals()

    return modname

###This is where you put the dictionary path ###
psource( '/Users/Documents/maya/2017/scripts/YiyangTools/Yang_NormalTranslatorUI.py' )

Yang_NormalTranslatorUI.launchUI()

"

How to use the tools:

pro::upon starting the tool it will create a nurbs sphere and its Material. This sphere is used in the Spherize tool.
		Selection has a limit amount, if over amount, the tool will not preform an action
Line 1 is for the title name of this tool
Line 2 would be a line of radio buttons, they will effect what the spinboxes and buttons in line 3-5 do
The Three Spinboxes represent the Relative Value of XYZ that will take effect on the normals upon selection
The "Def" buttons on the left are used to set the spinbox values to the default value(usually 0 or 1 depending on the tool).
	There is also a "Default" button bellow that sets all values to its default
The buttons on the right are used to add values to the spin boxes, the "-" button can effect whether you want to add in or subtract a value.
Radio buttons:
1 Add: adds a vector to the normals
2 Multiply: Multiplies each x y z to the normals(not to be confused with other vector math). Default is [1,1,1]
3 Rotate: Rotates the angle by a degree(-180 to 180)
4 Replace: Type in the value and it will replace the normal with the vector you typed in.(when you type in (0,0,0),it will cause issues)
5 Average: For each Vertex, get the average value and lerp it in x y z
6 Spherize: The Blue Sphere is displayed and can be selected when pressing the Sphere button. The blue sphere is used as a target for the function, 
	by moving the sphere you will change where the normals point at. scaling and rotating will not affect the results. The select button will select 
	the last selection you have selected. The Center button is used for placing the sphere. the sphere will go the coordanates of the last 
	object(or component) of the current selection. When XYZ is all 1, normals will be rays from Sphere Coordanates. This tool may be buggy.
	
	If switching between tools cause issues, press Origin in Line 6 and Apply, and then put the scroll bar in Line 6 to where it was.
	
Line 6: The Slider is used for Switching between the original Normals and the Targeted normals.
Line 7-9:
	1. Default: sets all the spinbox values to default
	2. Display: Toggles the display of vertex normals of an object. "-"will *√(1/2) "+" will *√(2) which is basically halfway through *0.5 or *2.
	3. Live: Turn off for some functions that may cause problems when the tool is open.(The tool reacts to selections) Turning off Live may cause problems.
	4. HardEdges: takes the value in the spinbox on the right as an angle limit between soft and hard edges. Basically the "Soft/Hard Edge" tool 
		in Default Maya. (Auto unlocks normals)
	5. Apply: applies the tool. If you don't apply the normals will pop back to what they were when you change a selection or close the tool.
	6. NrmtoCol,ColtoNrm,EmptyCol: these tools transfer back and forth from vertex normals and vertex colour(sorry I'm not American). EmptyCol deletes 
		all the vertex colour information.

		if you have trouble closing the window. rerun the script to open the tool and then close it.(It seems to be an issue with 2017 Update 4)
		
		
Update:
For those who have a problem linking the two files together
for example getting an errors like
"# AttributeError: 'module' object has no attribute 'ApplyNormals'"
open the file "Yang_NormalTranslaterTool_1file_ver.py"
and copy all the text to the Script Editor then run.
you can make that to a shelf tool as well！

Thank you for your time, have fun!
		
#--------------------------------------------------------------------------
#
# 脚本名称	 : 法线编辑工具Beta1.0
# 内容	     : 法线编辑
# 作者  	 : 则远霄汉
# 更新  	 : 2017/7/8
# 备注	     : 感谢 Charlie McKenna的指导
#			   
#--------------------------------------------------------------------------
#####事前读
十分感谢让我有机会给你提供这个Maya工具。此工具为鄙人首次用python在Maya制作工具，如有问题请联系邮箱yiyangchen@gmail.com或者Q：1047397344
安装过程：
1. 请把文件放入你想要的文件夹，个人建议 '/Users/Documents/maya/2017/scripts/YiyangTools/'
2. 在Maya右下角脚本编辑器输入此代码启动（也可以置入工具箱，注意是Python一栏，不要引号）：
"

import sys
import os
 
def psource(module):

    file = os.path.basename( module )
    dir = os.path.dirname( module )

    toks = file.split( '.' )
    modname = toks[0]


    if( os.path.exists( dir ) ):
        paths = sys.path
        pathfound = 0
        for path in paths:
            if(dir == path):
                pathfound = 1

        if not pathfound:
            sys.path.append( dir )

    exec ('import ' + modname) in globals()

    exec( 'reload( ' + modname + ' )' ) in globals()

    return modname

###此为路径，若此信息影响启动，请删除  或者在第一行写 “# -*- coding: UTF-8 -*- ” ###
psource( '/Users/Documents/maya/2017/scripts/YiyangTools/Yang_NormalTranslatorUI.py' )

Yang_NormalTranslatorUI.launchUI()

"
使用方法：
前：工具启动会自己生成球体和相应材质，球体为Spherize的目标。 选项有上限，如果选项数量超过一定数值会停止操作。
行1：工具的标题
行2：一排工具选项，工具会影响到行3-5的作用。
三个数字框对应三轴XYZ相对数值
“Def”会把数值归零缺省（根据工具选项一般为1或0）
右边的按钮大部分情况下影响数字框的数值（特殊情况下面有说明）
工具为：
	1 Add: 法线加上向量
	2 Multiply: 法线XYZ各个乘以数值（并非向量积） 缺省值为[1,1,1]
	3 Rotate: 法线旋转，范围为(-180， 180)
	4 Replace: 向量替换法线(输入为(0,0,0)的时候会出现问题，这时候点Origin)
	5 Average: 每个定点向量平均化，xyz是接近平均程度
	6 Spherize: 会显示蓝色球体，蓝色球体是目标。xyz是程度，当XYZ都为1，法线就会是从目标向外的射线。-1为向内。球体的位置会影响法线，大小和旋转不会。
		Sphere按钮会让你选择球体，Select按钮会返回到你刚才的（定点）选项，Center按钮会把球体放置在你现在选项中的最后一个选项。此工具可能不完善。
		
	如果工具切换期间出现问题，点一下行6的Origin然后点Apply，接着把滑条拉掉原来的位置。

行6为原本法线和目标法线的滑条。两个按钮为两个极端值。
行7-9为其他工具:
	1. Default: XYZ数字框全部归零缺省
	2. Display: 切换显示定点法线 "-"会将显示法线 *√(1/2) "+" 会 *√(2) 就是 *0.5 或者 *2 的中间值.
	3. Live: 由于工具窗口会监事你的选项，会影响到其他的的操作，故进行其他操作可以关闭Live。如果关着操作工具可能会引发问题
	4. HardEdges: 和Maya自带的硬边法线，软边法线一样，有时候要按两次 (自动解锁法线)
	5. Apply: 实行工具，如果不实行法线改变将会在你有新的选项或者关闭工具后无效。
	6. NrmtoCol,ColtoNrm,EmptyCol: 会将顶点法线和顶点颜色相互切换，EmptyCol会清空顶点颜色
	
某些版本关闭会有些问题，请再次运行开启脚本，再关闭。
	
更新:
那些无法关联两个文件的用户，得到类似这样的报错
"# AttributeError: 'module' object has no attribute 'ApplyNormals'"
解决方案是记事本打开 "Yang_NormalTranslaterTool_1file_ver.py"
全部复制到Script Editor运行.
可以做成工具栏的工具哦！
	
那么其他没什么了，感谢使用！我会加油努力的！
