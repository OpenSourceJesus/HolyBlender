using System;
using System.Diagnostics;
using System.Runtime.InteropServices;

namespace TriLibCore.Samples
{
    public class RuntimeProcessUtils
    {
#if UNITY_EDITOR_WIN || UNITY_STANDALONE_WIN
        [DllImport("psapi.dll", SetLastError = true)]
        private static extern bool GetProcessMemoryInfo(IntPtr hProcess, out PROCESS_MEMORY_COUNTERS counters, int size);

        [StructLayout(LayoutKind.Sequential, Size = 72)]
        private struct PROCESS_MEMORY_COUNTERS
        {
            public uint cb;
            public uint PageFaultCount;
            public UInt64 PeakWorkingSetSize;
            public UInt64 WorkingSetSize;
            public UInt64 QuotaPeakPagedPoolUsage;
            public UInt64 QuotaPagedPoolUsage;
            public UInt64 QuotaPeakNonPagedPoolUsage;
            public UInt64 QuotaNonPagedPoolUsage;
            public UInt64 PagefileUsage;
            public UInt64 PeakPagefileUsage;
        }

        public static long GetProcessMemory()
        {
            if (GetProcessMemoryInfo(Process.GetCurrentProcess().Handle, out var processMemoryCounters, Marshal.SizeOf<PROCESS_MEMORY_COUNTERS>()))
            {
                var memoryUsage = processMemoryCounters.WorkingSetSize;
                return (long)memoryUsage;
            }
            return 0;
        }
#else
        public static long GetProcessMemory()
        {
            return 0;
        }
#endif
    }
}