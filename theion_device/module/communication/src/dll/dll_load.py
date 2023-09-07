import ctypes
import os


def get_keyence_lib():
    dll_dir = os.path.abspath(os.path.dirname(__file__))
    dll_path = os.path.join(dll_dir, "keyenceLib.dll")
    os.chdir(dll_dir)

    if not os.path.exists(dll_path):
        # Give up if none of the above succeeded:
        raise Exception("Could not locate " + dll_path)

    keyence_lib = ctypes.cdll.LoadLibrary(dll_path)
    keyence_lib.keyence_connect.argtypes = (ctypes.c_wchar_p,)
    keyence_lib.keyence_connect.restype = ctypes.c_wchar_p
    keyence_lib.keyence_get_current_state.restype = ctypes.c_wchar_p
    keyence_lib.get_data.restype = ctypes.c_double
    keyence_lib.keyence_disconnect.restype = ctypes.c_wchar_p

    return keyence_lib


def get_meteor_lib():
    dll_dir = os.path.abspath(os.path.dirname(__file__))
    dll_path = os.path.join(dll_dir, "MeteorPrintEngineApi.dll")
    meteor_lib = ctypes.cdll.LoadLibrary(dll_path)

    meteor_lib.initialize_printer.argtypes = (
        ctypes.c_char_p,
        ctypes.c_uint32,
        ctypes.c_ulong,
    )
    meteor_lib.initialize_printer.restype = ctypes.c_char_p

    meteor_lib.trigger.restype = ctypes.c_char_p

    meteor_lib.stop_printer.restype = ctypes.c_char_p

    meteor_lib.upload_image.argtypes = (
        ctypes.c_char_p,
        ctypes.c_ulong,
    )
    meteor_lib.upload_image.restype = ctypes.c_char_p

    return meteor_lib


if __name__ == "__main__":
    key_lib = get_keyence_lib()
    # res = key_lib.keyence_connect("192.168.0.105")
    # print(res)
    """ lib = get_meteor_lib()
    try:
        file_name = b"C:\\Users\\PrintHead\\Desktop\\THEION\\MeteorAPI\\images\\img_n0_g0_s300_t8_f6000_d39.36.png"
        result = lib.initialize_printer(
            b"C:\\Users\\PrintHead\\Desktop\\THEION\\MeteorAPI\\images\\img_n0_g0_s300_t8_f6000_d39.36.png",
            6000,
            50,
        )
        print(result.decode())
        result = lib.stop_printer()
        print(result.decode())

        result = lib.trigger()
        print(result.decode())
    except Exception as e:
        print(repr(e))"""
