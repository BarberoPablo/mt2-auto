using System;
using System.Runtime.InteropServices;

class Program
{
    const int WM_LBUTTONDOWN = 0x0201;
    const int WM_LBUTTONUP = 0x0202;
    const int MK_LBUTTON = 0x0001;

    [DllImport("user32.dll", SetLastError = true, CharSet = CharSet.Auto)]
    static extern IntPtr FindWindow(string? lpClassName, string? lpWindowName);

    [DllImport("user32.dll")]
    static extern bool PostMessage(IntPtr hWnd, uint Msg, IntPtr wParam, IntPtr lParam);

    [DllImport("user32.dll")]
    static extern bool ScreenToClient(IntPtr hWnd, ref POINT lpPoint);

    [StructLayout(LayoutKind.Sequential)]
    struct POINT
    {
        public int X;
        public int Y;
    }

    static void Main(string[] args)
    {
        if (args.Length < 2)
        {
            Console.WriteLine("Uso: MetinClicker.exe <x> <y> [window_title]");
            Console.WriteLine("Ejemplo: MetinClicker.exe 500 400 Elveron");
            return;
        }

        if (!int.TryParse(args[0], out int screenX) || !int.TryParse(args[1], out int screenY))
        {
            Console.WriteLine("❌ Coordenadas inválidas.");
            return;
        }

        // Window title is optional, defaults to "Elveron" for backwards compatibility
        string windowTitle = args.Length >= 3 ? args[2] : "Elveron";

        Console.WriteLine($"Buscando ventana '{windowTitle}'...");
        IntPtr hWnd = FindWindow(null, windowTitle);

        if (hWnd == IntPtr.Zero)
        {
            Console.WriteLine($"❌ No se encontró la ventana '{windowTitle}'.");
            Console.WriteLine("💡 Asegúrate de que el título de la ventana coincida exactamente.");
            return;
        }

        Console.WriteLine("✅ Ventana encontrada!");

        // Convert screen coordinates to client coordinates (relative to the window)
        POINT point = new POINT { X = screenX, Y = screenY };
        ScreenToClient(hWnd, ref point);

        int clientX = point.X;
        int clientY = point.Y;

        // lParam format: low word = X, high word = Y
        IntPtr lParam = (IntPtr)((clientY << 16) | (clientX & 0xFFFF));

        // Send mouse down message
        bool downSuccess = PostMessage(hWnd, WM_LBUTTONDOWN, (IntPtr)MK_LBUTTON, lParam);
        
        // Small delay to simulate a real click
        System.Threading.Thread.Sleep(10);
        
        // Send mouse up message
        bool upSuccess = PostMessage(hWnd, WM_LBUTTONUP, IntPtr.Zero, lParam);

        if (downSuccess && upSuccess)
        {
            Console.WriteLine($"✔️ Clic enviado en x={screenX}, y={screenY} (client: {clientX}, {clientY})!");
        }
        else
        {
            Console.WriteLine($"⚠️ Advertencia: El mensaje podría no haberse enviado correctamente.");
        }
    }
}







/* Mouse moving to coords correctly 

using System;
using System.Runtime.InteropServices;

class Program
{
    [StructLayout(LayoutKind.Sequential)]
    struct INPUT
    {
        public int type;
        public MOUSEINPUT mi;
    }

    [StructLayout(LayoutKind.Sequential)]
    struct MOUSEINPUT
    {
        public int dx;
        public int dy;
        public uint mouseData;
        public uint dwFlags;
        public uint time;
        public IntPtr dwExtraInfo;
    }

    const int INPUT_MOUSE = 0;
    const uint MOUSEEVENTF_MOVE = 0x0001;
    const uint MOUSEEVENTF_ABSOLUTE = 0x8000;
    const uint MOUSEEVENTF_LEFTDOWN = 0x0002;
    const uint MOUSEEVENTF_LEFTUP = 0x0004;

    [DllImport("user32.dll")]
    static extern uint SendInput(uint nInputs, INPUT[] pInputs, int cbSize);

    [DllImport("user32.dll")]
    static extern int GetSystemMetrics(int nIndex);
    const int SM_CXSCREEN = 0;
    const int SM_CYSCREEN = 1;

    static void Main(string[] args)
    {
        if (args.Length < 2)
        {
            Console.WriteLine("Uso: MetinClicker.exe <x> <y>");
            return;
        }

        if (!int.TryParse(args[0], out int screenX) || !int.TryParse(args[1], out int screenY))
        {
            Console.WriteLine("Coordenadas inválidas.");
            return;
        }

        int screenWidth = GetSystemMetrics(SM_CXSCREEN);
        int screenHeight = GetSystemMetrics(SM_CYSCREEN);

        int absoluteX = (int)(screenX * 65535 / (double)screenWidth);
        int absoluteY = (int)(screenY * 65535 / (double)screenHeight);

        INPUT[] inputs = new INPUT[2];

        inputs[0] = new INPUT
        {
            type = INPUT_MOUSE,
            mi = new MOUSEINPUT
            {
                dx = absoluteX,
                dy = absoluteY,
                dwFlags = MOUSEEVENTF_ABSOLUTE | MOUSEEVENTF_MOVE | MOUSEEVENTF_LEFTDOWN,
                mouseData = 0,
                time = 0,
                dwExtraInfo = IntPtr.Zero
            }
        };

        inputs[1] = new INPUT
        {
            type = INPUT_MOUSE,
            mi = new MOUSEINPUT
            {
                dx = absoluteX,
                dy = absoluteY,
                dwFlags = MOUSEEVENTF_ABSOLUTE | MOUSEEVENTF_MOVE | MOUSEEVENTF_LEFTUP,
                mouseData = 0,
                time = 0,
                dwExtraInfo = IntPtr.Zero
            }
        };

        SendInput((uint)inputs.Length, inputs, Marshal.SizeOf(typeof(INPUT)));

        Console.WriteLine($"✔️ Clic enviado en x={screenX}, y={screenY}!");
    }
}
*/



/* #Working .exe alone code
using System;
using System.Runtime.InteropServices;
using System.Threading;

class Program
{
    const int WM_LBUTTONDOWN = 0x0201;
    const int WM_LBUTTONUP = 0x0202;
    const int MK_LBUTTON = 0x0001;

    [DllImport("user32.dll", SetLastError = true)]
    static extern IntPtr FindWindow(string lpClassName, string lpWindowName);

    [DllImport("user32.dll")]
    static extern bool PostMessage(IntPtr hWnd, uint Msg, IntPtr wParam, IntPtr lParam);

    static void Main()
    {
        Console.WriteLine("Buscando ventana de Elveron...");
        // ⚠️ Asegurate que el título de la ventana coincida con el que ves en la barra superior
        IntPtr hWnd = FindWindow(null, "Elveron");

        if (hWnd == IntPtr.Zero)
        {
            Console.WriteLine("❌ No se encontró la ventana del juego.");
            Console.ReadLine();
            return;
        }

        Console.WriteLine("✅ Ventana encontrada!");
        Console.WriteLine("Esperando 3 segundos...");
        Thread.Sleep(3000);

        // Simula clic en el centro de la pantalla (x=500, y=400 por ejemplo)
        int x = 500;
        int y = 400;

        IntPtr lParam = (IntPtr)((y << 16) | (x & 0xFFFF));

        PostMessage(hWnd, WM_LBUTTONDOWN, (IntPtr)MK_LBUTTON, lParam);
        PostMessage(hWnd, WM_LBUTTONUP, IntPtr.Zero, lParam);

        Console.WriteLine("✔️ Clic enviado a la ventana!");
        Console.ReadLine();
    }
}
 */