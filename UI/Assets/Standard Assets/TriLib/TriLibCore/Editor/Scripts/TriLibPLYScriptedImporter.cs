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
#if !TRILIB_DISABLE_EDITOR_PLY_IMPORT
    [ScriptedImporter(2, new[] { "ply" })]
#endif
    public class TriLibPLYScriptedImporter : TriLibScriptedImporter
    {

    }
	
	[CustomEditor(typeof(TriLibPLYScriptedImporter))]
    public class TriLibPLYImporterEditor : ScriptedImporterEditor
    {
        private int _currentTab;

        protected override Type extraDataType => typeof(AssetLoaderOptions);

        protected override void InitializeExtraDataInstance(Object extraData, int targetIndex)
        {
            var scriptedImporter = (TriLibPLYScriptedImporter) target;
            var existingAssetLoaderOptions = scriptedImporter.AssetLoaderOptions;
            EditorUtility.CopySerializedIfDifferent(existingAssetLoaderOptions, extraData);
        }

        protected override void Apply()
        {
            base.Apply();
            var assetLoaderOptions = (AssetLoaderOptions) extraDataTarget;
            var scriptedImporter = (TriLibPLYScriptedImporter) target;
            scriptedImporter.AssetLoaderOptions = assetLoaderOptions;
        }

        public override void OnInspectorGUI()
        {
            AssetLoaderOptionsEditor.ShowInspectorGUI(extraDataSerializedObject, ref _currentTab);
            ApplyRevertGUI();
        }
    }
}