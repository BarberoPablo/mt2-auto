using System;
using System.Runtime.InteropServices;
using System.Threading;

class Program
{
    const int WM_LBUTTONDOWN = 0x0201;
    const int WM_LBUTTONUP = 0x0202;
    const int MK_LBUTTON = 0x0001;
    const int SW_RESTORE = 9;

    [DllImport("user32.dll", SetLastError = true, CharSet = CharSet.Auto)]
    static extern IntPtr FindWindow(string? lpClassName, string? lpWindowName);
    [DllImport("user32.dll")]
    static extern bool PostMessage(IntPtr hWnd, uint Msg, IntPtr wParam, IntPtr lParam);
    [DllImport("user32.dll")]
    static extern bool ScreenToClient(IntPtr hWnd, ref POINT lpPoint);
    [DllImport("user32.dll")]
    static extern bool SetForegroundWindow(IntPtr hWnd);
    [DllImport("user32.dll")]
    static extern bool BringWindowToTop(IntPtr hWnd);
    [DllImport("user32.dll")]
    static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
    [DllImport("user32.dll")]
    static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint lpdwProcessId);
    [DllImport("kernel32.dll")]
    static extern uint GetCurrentThreadId();
    [DllImport("user32.dll")]
    static extern bool AttachThreadInput(uint idAttach, uint idAttachTo, bool fAttach);

    [StructLayout(LayoutKind.Sequential)]
    struct POINT
    {
        public int X;
        public int Y;
    }

    static void Main(string[] args)
    {
        if (args.Length == 0)
        {
            Console.WriteLine("Uso:");
            Console.WriteLine("  MetinClicker.exe focus [window_title]");
            Console.WriteLine("  MetinClicker.exe click <x> <y> [window_title]");
            return;
        }

        string command = args[0].ToLower();

        switch (command)
        {
            case "focus":
                string focusTitle = args.Length >= 2 ? args[1] : "Elveron";
                FocusWindow(focusTitle);
                break;

            case "click":
                if (args.Length < 3)
                {
                    Console.WriteLine("Uso: MetinClicker.exe click <x> <y> [window_title]");
                    return;
                }
                if (!int.TryParse(args[1], out int screenX) || !int.TryParse(args[2], out int screenY))
                {
                    Console.WriteLine("❌ Coordenadas inválidas.");
                    return;
                }
                string clickTitle = args.Length >= 4 ? args[3] : "Elveron";
                ClickInWindow(clickTitle, screenX, screenY);
                break;

            default:
                Console.WriteLine($"Comando desconocido: {command}");
                break;
        }
    }

    static IntPtr GetWindowHandle(string windowTitle)
    {
        IntPtr hWnd = FindWindow(null, windowTitle);
        if (hWnd == IntPtr.Zero)
        {
            Console.WriteLine($"❌ No se encontró la ventana '{windowTitle}'.");
        }
        return hWnd;
    }

    public static void FocusWindow(string windowTitle)
    {
        IntPtr hWnd = GetWindowHandle(windowTitle);
        if (hWnd == IntPtr.Zero) return;

        ShowWindow(hWnd, SW_RESTORE);
        uint winThread = GetWindowThreadProcessId(hWnd, out _);
        uint curThread = GetCurrentThreadId();

        bool attached = false;
        if (winThread != curThread)
            attached = AttachThreadInput(curThread, winThread, true);

        SetForegroundWindow(hWnd);
        BringWindowToTop(hWnd);
        Thread.Sleep(100);

        if (attached)
            AttachThreadInput(curThread, winThread, false);

        Console.WriteLine($"✅ Ventana '{windowTitle}' enfocada correctamente.");
    }

    public static void ClickInWindow(string windowTitle, int screenX, int screenY)
    {
        IntPtr hWnd = GetWindowHandle(windowTitle);
        if (hWnd == IntPtr.Zero) return;

        POINT point = new POINT { X = screenX, Y = screenY };
        ScreenToClient(hWnd, ref point);
        IntPtr lParam = (IntPtr)((point.Y << 16) | (point.X & 0xFFFF));

        PostMessage(hWnd, WM_LBUTTONDOWN, (IntPtr)MK_LBUTTON, lParam);
        Thread.Sleep(10);
        PostMessage(hWnd, WM_LBUTTONUP, IntPtr.Zero, lParam);

        Console.WriteLine($"✔️ Click enviado en ({screenX}, {screenY}) dentro de '{windowTitle}'.");
    }
}
