
#ifndef _INTERFACE_H
#define _INTERFACE_H


#ifdef BUILD_DLL  
#define DLL_EXPORT __declspec(dllexport)  
#else  
#define DLL_EXPORT __declspec(dllimport)  
#endif 

#ifdef __cplusplus  
extern "C"
{
#endif

	/**
	* 相关使用方法请参考相关的DEMO示例
	*/

	//获取电脑中可用的串口序号
	DLL_EXPORT int __stdcall GetDeviceList(char* pDeviceList, int len);
	//打开串口
	DLL_EXPORT int __stdcall OpenDevice(int port);
	//关闭串口
	DLL_EXPORT void __stdcall CloseDevice(int device);
	//获取设备的USB口数量
	DLL_EXPORT int __stdcall GetDeviceUSBCount(int device);
	//获取设备的ID号，pDeviceId长度需为12
	DLL_EXPORT int __stdcall GetDeviceId(int device, char* pDeviceId, int len);
	//获取设备的USB口状态，pStatus长度需为64,代表64个点的状态
	DLL_EXPORT int __stdcall GetDeviceStatus(int device, char* pStatus, int len);
	//设置设备的USB口状态，pStatus长度需为64,代表64个点的状态
	DLL_EXPORT int __stdcall WriteDevice(int device, char* pOut, int len);


#ifdef __cplusplus  
}
#endif

#endif //_INTERFACE_H
