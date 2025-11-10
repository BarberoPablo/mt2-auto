using System;
using System.Runtime.InteropServices;
using System.Threading;

class Program
{
    const int WM_LBUTTONDOWN = 0x0201;
    const int WM_LBUTTONUP = 0x0202;
    const int MK_LBUTTON = 0x0001;

    const int SW_RESTORE = 9;
    const uint SWP_NOSIZE = 0x0001;
    const uint SWP_NOMOVE = 0x0002;
    const uint SWP_SHOWWINDOW = 0x0040;

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

        // Focusing the window
        try
        {
            // Restore (si está minimizada)
            ShowWindow(hWnd, SW_RESTORE);

            // Traer al frente usando AttachThreadInput para saltar restricciones de foreground window
            uint windowThreadId = GetWindowThreadProcessId(hWnd, out _);
            uint currentThreadId = GetCurrentThreadId();

            bool attached = false;
            if (windowThreadId != currentThreadId)
            {
                attached = AttachThreadInput(currentThreadId, windowThreadId, true);
            }

            // Intentos para asegurar que la ventana queda en foreground
            if (!SetForegroundWindow(hWnd))
            {
                Console.WriteLine("⚠️ SetForegroundWindow falló en el primer intento, intentando BringWindowToTop...");
                BringWindowToTop(hWnd);
                SetForegroundWindow(hWnd);
            }

            // Desprender AttachThreadInput si se había unido
            if (attached)
            {
                AttachThreadInput(currentThreadId, windowThreadId, false);
            }

            // Pequeña pausa para que Windows actualice el foco/estado
            Thread.Sleep(80);
        }
        catch (Exception ex)
        {
            Console.WriteLine("⚠️ Error al intentar dar foco a la ventana: " + ex.Message);
            // seguimos de todas formas, el resto del flujo intentará mandar mensajes
        }

        // Convert screen coordinates to client coordinates (relative to the window)
        POINT point = new POINT { X = screenX, Y = screenY };
        if (!ScreenToClient(hWnd, ref point))
        {
            Console.WriteLine("⚠️ ScreenToClient devolvió false. Las coordenadas pueden ser inválidas.");
        }

        int clientX = point.X;
        int clientY = point.Y;

        IntPtr lParam = (IntPtr)((clientY << 16) | (clientX & 0xFFFF));

        bool downSuccess = PostMessage(hWnd, WM_LBUTTONDOWN, (IntPtr)MK_LBUTTON, lParam);

        Thread.Sleep(10);

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