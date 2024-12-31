using System.Globalization;
using UnityEditor;
using UnityEditor.Build;
using UnityEditor.Build.Reporting;

public class StandaloneFileBrowserPreprocessor : IPreprocessBuildWithReport
{
    private const string CPUPlatformData = "CPU";
    private const string AnyCPUPlatformData = "AnyCPU";

    public int callbackOrder { get; }

    public void OnPreprocessBuild(BuildReport report)
    {
        var plugins = PluginImporter.GetAllImporters();
        foreach (var plugin in plugins)
        {
            // fixes a bug in Unity that resets the StandaloneFileBrowser plugin target CPU on OSX
            if (report.summary.platform == BuildTarget.StandaloneOSX && plugin.assetPath.EndsWith("standalonefilebrowser.bundle", true, CultureInfo.InvariantCulture))
            {
                var platformData = plugin.GetPlatformData("OSXUniversal", CPUPlatformData);
                if (!plugin.GetCompatibleWithPlatform(report.summary.platform) || platformData != AnyCPUPlatformData)
                {
                    if (EditorUtility.DisplayDialog(
                            $"StandaloneFileBrowser plugin is not included in '{report.summary.platform}' 'Any CPU' compilation.",
                            $"Do you want TriLib to configure the StandaloneFileBrowser plugin to be included in '{report.summary.platform}' 'Any CPU' compilation?",
                            "Yes", "No")
                    ) {
                        plugin.SetCompatibleWithPlatform(report.summary.platform, true);
                        plugin.SetPlatformData("OSXUniversal", CPUPlatformData, AnyCPUPlatformData);
                        plugin.SaveAndReimport();
                    }
                }
                break;
            }
        }
    }
}