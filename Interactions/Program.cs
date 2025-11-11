using System;
using System.Runtime.InteropServices;
using System.Threading;

class Program
{
    // === Win32 Constants ===
    const int WM_LBUTTONDOWN = 0x0201;
    const int WM_LBUTTONUP = 0x0202;
    const int MK_LBUTTON = 0x0001;
    const int SW_RESTORE = 9;
    const uint INPUT_MOUSE = 0;
    const uint MOUSEEVENTF_LEFTDOWN = 0x0002;
    const uint MOUSEEVENTF_LEFTUP = 0x0004;

    // === Win32 Imports ===
    [DllImport("user32.dll")] static extern bool SetForegroundWindow(IntPtr hWnd);
    [DllImport("user32.dll")] static extern bool BringWindowToTop(IntPtr hWnd);
    [DllImport("user32.dll")] static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
    [DllImport("user32.dll")] static extern IntPtr FindWindow(string? lpClassName, string? lpWindowName);
    [DllImport("user32.dll")] static extern bool PostMessage(IntPtr hWnd, uint Msg, IntPtr wParam, IntPtr lParam);
    [DllImport("user32.dll")] static extern bool ScreenToClient(IntPtr hWnd, ref POINT lpPoint);
    [DllImport("user32.dll")] static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint lpdwProcessId);
    [DllImport("kernel32.dll")] static extern uint GetCurrentThreadId();
    [DllImport("user32.dll")] static extern bool AttachThreadInput(uint idAttach, uint idAttachTo, bool fAttach);

    [DllImport("user32.dll", SetLastError = true)]
    static extern uint SendInput(uint nInputs, INPUT[] pInputs, int cbSize);

    // === Structs ===
    [StructLayout(LayoutKind.Sequential)]
    struct POINT { public int X; public int Y; }

    [StructLayout(LayoutKind.Sequential)]
    struct INPUT { public uint type; public InputUnion u; }

    [StructLayout(LayoutKind.Explicit)]
    struct InputUnion { [FieldOffset(0)] public MOUSEINPUT mi; }

    [StructLayout(LayoutKind.Sequential)]
    struct MOUSEINPUT
    {
        public int dx; public int dy; public uint mouseData;
        public uint dwFlags; public uint time; public IntPtr dwExtraInfo;
    }

    static void PrintUsage()
    {
        Console.WriteLine("Uso:");
        Console.WriteLine("  Clicker.exe focus [window_title]");
        Console.WriteLine("  Clicker.exe click <x> <y> [window_title]");
        Console.WriteLine("  Clicker.exe click_mouse");
    }

    // === Funciones ===
    static void FocusWindow(string title)
    {
        IntPtr hWnd = FindWindow(null, title);
        if (hWnd == IntPtr.Zero) { Console.WriteLine($"❌ No se encontró la ventana '{title}'"); return; }

        ShowWindow(hWnd, SW_RESTORE);
        uint winThread = GetWindowThreadProcessId(hWnd, out _);
        uint curThread = GetCurrentThreadId();
        bool attached = false;
        if (winThread != curThread) attached = AttachThreadInput(curThread, winThread, true);

        SetForegroundWindow(hWnd);
        BringWindowToTop(hWnd);
        Thread.Sleep(100);
        if (attached) AttachThreadInput(curThread, winThread, false);

        Console.WriteLine($"✅ Ventana '{title}' enfocada.");
    }

    static void ClickInWindow(string title, int screenX, int screenY)
    {
        IntPtr hWnd = FindWindow(null, title);
        if (hWnd == IntPtr.Zero) { Console.WriteLine($"❌ No se encontró la ventana '{title}'"); return; }

        POINT pt = new POINT { X = screenX, Y = screenY };
        ScreenToClient(hWnd, ref pt);
        IntPtr lParam = (IntPtr)((pt.Y << 16) | (pt.X & 0xFFFF));

        PostMessage(hWnd, WM_LBUTTONDOWN, (IntPtr)MK_LBUTTON, lParam);
        Thread.Sleep(10);
        PostMessage(hWnd, WM_LBUTTONUP, IntPtr.Zero, lParam);

        Console.WriteLine($"✔️ Click enviado en ({screenX},{screenY}) en '{title}'.");
    }

    static void ClickCurrentPosition()
    {
        INPUT[] inputs = new INPUT[2];
        inputs[0].type = INPUT_MOUSE; inputs[0].u.mi.dwFlags = MOUSEEVENTF_LEFTDOWN;
        inputs[1].type = INPUT_MOUSE; inputs[1].u.mi.dwFlags = MOUSEEVENTF_LEFTUP;
        SendInput((uint)inputs.Length, inputs, Marshal.SizeOf(typeof(INPUT)));
        Console.WriteLine("✔️ Click en la posición actual del mouse.");
    }

    static void ClickMouseOSK()
    {
        // Evento DOWN
        INPUT down = new INPUT();
        down.type = INPUT_MOUSE;
        down.u.mi = new MOUSEINPUT { dwFlags = MOUSEEVENTF_LEFTDOWN };

        // Evento UP
        INPUT up = new INPUT();
        up.type = INPUT_MOUSE;
        up.u.mi = new MOUSEINPUT { dwFlags = MOUSEEVENTF_LEFTUP };

        // Enviar DOWN
        uint resultDown = SendInput(1, new INPUT[] { down }, Marshal.SizeOf(typeof(INPUT)));
        if (resultDown == 0)
        {
            Console.WriteLine("❌ Error al enviar el DOWN del click.");
            return;
        }

        // Espera mínima para que la app detecte la pulsación
        Thread.Sleep(50); // 50ms es suficiente

        // Enviar UP
        uint resultUp = SendInput(1, new INPUT[] { up }, Marshal.SizeOf(typeof(INPUT)));
        if (resultUp == 0)
            Console.WriteLine("❌ Error al enviar el UP del click.");
        else
            Console.WriteLine("✔️ Click completo en la posición actual del OSK.");
    }


    // === Main ===
    static void Main(string[] args)
    {
        if (args.Length == 0) { PrintUsage(); return; }

        string command = args[0].ToLower();
        switch (command)
        {
            case "focus":
                string title = args.Length >= 2 ? args[1] : "Elveron";
                FocusWindow(title);
                break;
            case "click":
                if (args.Length < 3) { Console.WriteLine("❌ Uso: click <x> <y> [window_title]"); return; }
                if (!int.TryParse(args[1], out int x) || !int.TryParse(args[2], out int y)) { Console.WriteLine("❌ Coordenadas inválidas."); return; }
                string clickTitle = args.Length >= 4 ? args[3] : null;
                if (clickTitle != null) ClickInWindow(clickTitle, x, y);
                else ClickCurrentPosition(); // Mantener compatibilidad
                break;
            case "osk_click":
                ClickMouseOSK();
                break;
            default:
                Console.WriteLine($"❌ Comando desconocido: {command}");
                break;
        }
    }
}
