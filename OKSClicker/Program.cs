using System;
using System.Runtime.InteropServices;
using System.Threading;

class Program
{
    [StructLayout(LayoutKind.Sequential)]
    struct INPUT
    {
        public uint type;
        public InputUnion u;
    }

    [StructLayout(LayoutKind.Explicit)]
    struct InputUnion
    {
        [FieldOffset(0)] public MOUSEINPUT mi;
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

    const uint INPUT_MOUSE = 0;
    const uint MOUSEEVENTF_LEFTDOWN = 0x0002;
    const uint MOUSEEVENTF_LEFTUP = 0x0004;

    [DllImport("user32.dll", SetLastError = true)]
    static extern uint SendInput(uint nInputs, INPUT[] pInputs, int cbSize);

    static void Main(string[] args)
    {
        Console.WriteLine("🖱️ Haciendo clic donde está el mouse...");
        ClickCurrentPosition();
        Console.WriteLine("✔️ Click enviado.");
    }

    static void ClickCurrentPosition()
    {
        INPUT[] inputs = new INPUT[2];

        inputs[0].type = INPUT_MOUSE;
        inputs[0].u.mi = new MOUSEINPUT
        {
            dwFlags = MOUSEEVENTF_LEFTDOWN
        };

        inputs[1].type = INPUT_MOUSE;
        inputs[1].u.mi = new MOUSEINPUT
        {
            dwFlags = MOUSEEVENTF_LEFTUP
        };

        uint result = SendInput((uint)inputs.Length, inputs, Marshal.SizeOf(typeof(INPUT)));

        if (result == 0)
            Console.WriteLine("❌ Error al enviar el click.");
    }
}
