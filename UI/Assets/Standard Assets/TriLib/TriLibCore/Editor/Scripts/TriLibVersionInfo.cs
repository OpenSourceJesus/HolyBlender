namespace TriLibCore.Editor
{
    public class TriLibVersionInfo
    {
        private static TriLibVersionInfo _instance;

        public string CurrentVersion
        {
            get
            {
                var assembly = System.Reflection.Assembly.GetAssembly(typeof(TriLibCore.ReaderBase));
                var fileVersionInfo = System.Diagnostics.FileVersionInfo.GetVersionInfo(assembly.Location);
                return fileVersionInfo.ProductVersion;
            }
        }

        public string SkipVersionInfoKey
        {
            get { return $"TriLibSkipVersionInfo{CurrentVersion}"; }
        }

        public static TriLibVersionInfo Instance
        {
            get
            {
                if (_instance == null)
                {
                    _instance = new TriLibVersionInfo();
                }
                return _instance;
            }
        }
    }
}