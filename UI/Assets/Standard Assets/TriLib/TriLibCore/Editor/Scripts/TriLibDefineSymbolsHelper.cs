using UnityEditor;
using UnityEditor.Build;

namespace TriLibCore.Editor
{
    public static class TriLibDefineSymbolsHelper
    {
        public static bool IsSymbolDefined(string targetDefineSymbol)
        {
#if UNITY_2020_3_OR_NEWER
            var buildTargetGroup = EditorUserBuildSettings.selectedBuildTargetGroup;
            var namedBuildTarget = NamedBuildTarget.FromBuildTargetGroup(buildTargetGroup);
            var defineSymbols = PlayerSettings.GetScriptingDefineSymbols(namedBuildTarget);
#else
            var defineSymbols = PlayerSettings.GetScriptingDefineSymbolsForGroup(EditorUserBuildSettings.selectedBuildTargetGroup);
#endif
            var defineSymbolsArray = defineSymbols.Split(';');
            for (var i = 0; i < defineSymbolsArray.Length; i++)
            {
                var defineSymbol = defineSymbolsArray[i];
                var trimmedDefineSymbol = defineSymbol.Trim();
                if (trimmedDefineSymbol == targetDefineSymbol)
                {
                    return true;
                }
            }
            return false;
        }

        public static void UpdateSymbol(string targetDefineSymbol, bool value)
        {
#if UNITY_2020_3_OR_NEWER
            var buildTargetGroup = EditorUserBuildSettings.selectedBuildTargetGroup;
            var namedBuildTarget = NamedBuildTarget.FromBuildTargetGroup(buildTargetGroup);
            var defineSymbols = PlayerSettings.GetScriptingDefineSymbols(namedBuildTarget);
#else
            var defineSymbols = PlayerSettings.GetScriptingDefineSymbolsForGroup(EditorUserBuildSettings.selectedBuildTargetGroup);
#endif
            var defineSymbolsArray = defineSymbols.Split(';');
            var newDefineSymbols = string.Empty;
            var isDefined = false;
            for (var i = 0; i < defineSymbolsArray.Length; i++)
            {
                var defineSymbol = defineSymbolsArray[i];
                var trimmedDefineSymbol = defineSymbol.Trim();
                if (trimmedDefineSymbol == targetDefineSymbol)
                {
                    if (!value)
                    {
                        continue;
                    }
                    isDefined = true;
                }
                newDefineSymbols += string.Format("{0};", trimmedDefineSymbol);
            }

            if (value && !isDefined)
            {
                newDefineSymbols += string.Format("{0};", targetDefineSymbol);
            }
#if UNITY_2020_3_OR_NEWER
            PlayerSettings.SetScriptingDefineSymbols(namedBuildTarget, newDefineSymbols);
#else
            PlayerSettings.SetScriptingDefineSymbolsForGroup(EditorUserBuildSettings.selectedBuildTargetGroup, newDefineSymbols);
#endif
        }
    }
}