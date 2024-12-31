#pragma warning disable CS0105
using System;
using UnityEditor;
using Object = UnityEngine.Object;
#if UNITY_2020_2_OR_NEWER
using UnityEditor.AssetImporters;
#else
using UnityEditor.Experimental.AssetImporters;
#endif
namespace TriLibCore.Editor
{
#if !TRILIB_DISABLE_EDITOR_3MF_IMPORT
    [ScriptedImporter(2, new[] { "3mf" })]
#endif
    public class TriLib3MFScriptedImporter : TriLibScriptedImporter
    {

    }
	
	[CustomEditor(typeof(TriLib3MFScriptedImporter))]
    public class TriLib3MFImporterEditor : ScriptedImporterEditor
    {
        private int _currentTab;

        protected override Type extraDataType => typeof(AssetLoaderOptions);

        protected override void InitializeExtraDataInstance(Object extraData, int targetIndex)
        {
            var scriptedImporter = (TriLib3MFScriptedImporter) target;
            var existingAssetLoaderOptions = scriptedImporter.AssetLoaderOptions;
            EditorUtility.CopySerializedIfDifferent(existingAssetLoaderOptions, extraData);
        }

        protected override void Apply()
        {
            base.Apply();
            var assetLoaderOptions = (AssetLoaderOptions) extraDataTarget;
            var scriptedImporter = (TriLib3MFScriptedImporter) target;
            scriptedImporter.AssetLoaderOptions = assetLoaderOptions;
        }

        public override void OnInspectorGUI()
        {
            AssetLoaderOptionsEditor.ShowInspectorGUI(extraDataSerializedObject, ref _currentTab);
            ApplyRevertGUI();
        }
    }
}