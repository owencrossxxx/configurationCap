function varargout = GUI(varargin)
% GUI MATLAB code for GUI.fig
%      GUI, by itself, creates a new GUI or raises the existing
%      singleton*.
%
%      H = GUI returns the handle to a new GUI or the handle to
%      the existing singleton*.
%
%      GUI('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in GUI.M with the given input arguments.
%
%      GUI('Property','Value',...) creates a new GUI or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before GUI_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to GUI_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help GUI

% Last Modified by GUIDE v2.5 24-May-2021 15:33:58

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @GUI_OpeningFcn, ...
                   'gui_OutputFcn',  @GUI_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before GUI is made visible.
function GUI_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to GUI (see VARARGIN)

% Choose default command line output for GUI
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes GUI wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = GUI_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on button press in initialize.
function initialize_Callback(hObject, eventdata, handles)
% hObject    handle to initialize (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

handles.output = hObject;
    handles.s = serialport("/dev/ttyACM0",9600);
%     while(1)
%     data = read(handles.s,8,"char");
%     pressure = zeros(1,1);
%         for i = 1
%             pressure(i) = 100*str2double(data(8*i-3))+10*str2double(data(8*i-2))+str2double(data(8*i-1))-(100*str2double(data(8*i-7))+10*str2double(data(8*i-6))+str2double(data(8*i-5)));
%         end
%     
%     set1(handles.p1,'string',num2str(pressure(1)* 0.0048828125 * 10.0683 ));
%     
%     end
while(1)

readings = [];
pressure = [];
    while(1)
        ch = read(handles.s,1,"char");
        readings = [readings ch];
        if ch == "!"
            if max(size(readings))>=15
            pos = [0 find(readings == ',') max(size(readings))];
            for i = 1:(length(pos)-1)
                pressure_temp = str2double(readings((pos(i)+1):pos(i+1)-1));
                pressure = [pressure pressure_temp];
            end
            set(handles.p1,'string',num2str(pressure(1)));
            set(handles.p2,'string',num2str(pressure(2)));
            set(handles.p3,'string',num2str(pressure(3)));
          end
            break
        end


    end
    guidata(hObject,handles);

end
guidata(hObject,handles);

    
    

function u1_Callback(hObject, eventdata, handles)
% hObject    handle to u1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of u1 as text
%        str2double(get(hObject,'String')) returns contents of u1 as a double
data2send = get(handles.u1,'String');
data2send = append("2;3;",data2send,";");
write(handles.s,data2send,'string');

% --- Executes during object creation, after setting all properties.
function u1_CreateFcn(hObject, eventdata, handles)
% hObject    handle to u1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function u2_Callback(hObject, eventdata, handles)
% hObject    handle to u2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of u2 as text
%        str2double(get(hObject,'String')) returns contents of u2 as a double
data2send = get(handles.u2,'String');
data2send = append("2;4;",data2send,";");
write(handles.s,data2send,'string');

% --- Executes during object creation, after setting all properties.
function u2_CreateFcn(hObject, eventdata, handles)
% hObject    handle to u2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function u3_Callback(hObject, eventdata, handles)
% hObject    handle to u3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of u3 as text
%        str2double(get(hObject,'String')) returns contents of u3 as a double
data2send = get(handles.u3,'String');
data2send = append("2;5;",data2send,";");
write(handles.s,data2send,'string');

% --- Executes during object creation, after setting all properties.
function u3_CreateFcn(hObject, eventdata, handles)
% hObject    handle to u3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function u4_Callback(hObject, eventdata, handles)
% hObject    handle to u4 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of u4 as text
%        str2double(get(hObject,'String')) returns contents of u4 as a double
data2send = get(handles.u4,'String');
data2send = append("2;6;",data2send,";");
write(handles.s,data2send,'string');

% --- Executes during object creation, after setting all properties.
function u4_CreateFcn(hObject, eventdata, handles)
% hObject    handle to u4 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function u5_Callback(hObject, eventdata, handles)
% hObject    handle to u5 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of u5 as text
%        str2double(get(hObject,'String')) returns contents of u5 as a double
data2send = get(handles.u5,'String');
data2send = append("2;7;",data2send,";");
write(handles.s,data2send,'string');

% --- Executes during object creation, after setting all properties.
function u5_CreateFcn(hObject, eventdata, handles)
% hObject    handle to u5 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function u6_Callback(hObject, eventdata, handles)
% hObject    handle to u6 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of u6 as text
%        str2double(get(hObject,'String')) returns contents of u6 as a double
data2send = get(handles.u6,'String');
data2send = append("2;8;",data2send,";");
write(handles.s,data2send,'string');


% --- Executes during object creation, after setting all properties.
function u6_CreateFcn(hObject, eventdata, handles)
% hObject    handle to u6 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function u7_Callback(hObject, eventdata, handles)
% hObject    handle to u7 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of u7 as text
%        str2double(get(hObject,'String')) returns contents of u7 as a double
data2send = get(handles.u7,'String');
data2send = append("2;9;",data2send,";");
write(handles.s,data2send,'string');

% --- Executes during object creation, after setting all properties.
function u7_CreateFcn(hObject, eventdata, handles)
% hObject    handle to u7 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function u8_Callback(hObject, eventdata, handles)
% hObject    handle to u8 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of u8 as text
%        str2double(get(hObject,'String')) returns contents of u8 as a double
data2send = get(handles.u8,'String');
data2send = append("2;10;",data2send,";");
write(handles.s,data2send,'string');

% --- Executes during object creation, after setting all properties.
function u8_CreateFcn(hObject, eventdata, handles)
% hObject    handle to u8 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function u9_Callback(hObject, eventdata, handles)
% hObject    handle to u9 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of u9 as text
%        str2double(get(hObject,'String')) returns contents of u9 as a double
data2send = get(handles.u9,'String');
data2send = append("2;11;",data2send,";");
write(handles.s,data2send,'string');

% --- Executes during object creation, after setting all properties.
function u9_CreateFcn(hObject, eventdata, handles)
% hObject    handle to u9 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in home.
function home_Callback(hObject, eventdata, handles)
% hObject    handle to home (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
write(handles.s,"253",'string');


% --- Executes on button press in set1.
function set1_Callback(hObject, eventdata, handles)
% hObject    handle to set1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
data2send = get(handles.u1,'String');
data2send = append("2;3;",data2send,";");
write(handles.s,data2send,'string');

function set2_Callback(hObject, eventdata, handles)
% hObject    handle to set1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
data2send = get(handles.u2,'String');
data2send = append("2;4;",data2send,";");
write(handles.s,data2send,'string');

function set3_Callback(hObject, eventdata, handles)
% hObject    handle to set1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
data2send = get(handles.u3,'String');
data2send = append("2;5;",data2send,";");
write(handles.s,data2send,'string');

function set4_Callback(hObject, eventdata, handles)
% hObject    handle to set1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
data2send = get(handles.u4,'String');
data2send = append("2;6;",data2send,";");
write(handles.s,data2send,'string');

function set5_Callback(hObject, eventdata, handles)
% hObject    handle to set1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
data2send = get(handles.u5,'String');
data2send = append("2;7;",data2send,";");
write(handles.s,data2send,'string');

function set6_Callback(hObject, eventdata, handles)
% hObject    handle to set1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
data2send = get(handles.u6,'String');
data2send = append("2;8;",data2send,";");
write(handles.s,data2send,'string');

function set7_Callback(hObject, eventdata, handles)
% hObject    handle to set1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
data2send = get(handles.u7,'String');
data2send = append("2;9;",data2send,";");
write(handles.s,data2send,'string');

function set8_Callback(hObject, eventdata, handles)
% hObject    handle to set1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
data2send = get(handles.u8,'String');
data2send = append("2;10;",data2send,";");
write(handles.s,data2send,'string');

function set9_Callback(hObject, eventdata, handles)
% hObject    handle to set1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
data2send = get(handles.u9,'String');
data2send = append("2;11;",data2send,";");
write(handles.s,data2send,'string');

% --- Executes on button press in stop.
function stop_Callback(hObject, eventdata, handles)
% hObject    handle to stop (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
write(handles.s,"255",'string');


% --- Executes on button press in calibrate.
function calibrate_Callback(hObject, eventdata, handles)
% hObject    handle to calibrate (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


% --- Executes on button press in set1.
