using System;
using System.Collections;
using TriLibCore.General;
using UnityEngine;

namespace TriLibCore.Mappers
{
    [Serializable]
    [CreateAssetMenu(menuName = "TriLib/Mappers/Material/Autodesk Interactive Standard Material Mapper", fileName = "AutodeskInteractiveStandardMaterialMapper")]
    public class AutodeskInteractiveStandardMaterialMapper : StandardMaterialMapper
    {
        public override bool UseShaderVariantCollection => true;

        public override string ShaderVariantCollectionPath => "Materials/Standard/AutodeskStandardShaderVariantCollection";

        public override Shader VariantCollectionShader => Shader.Find("Autodesk Interactive");

        public override Material MaterialPreset => null;

        public override Material CutoutMaterialPreset => null;

        public override Material TransparentComposeMaterialPreset => null;

        public override Material TransparentMaterialPreset => null;

        public override Material MaterialPresetNoMetallicTexture => null;

        public override Material CutoutMaterialPresetNoMetallicTexture => null;

        public override Material TransparentMaterialPresetNoMetallicTexture => null;

        public override Material TransparentComposeMaterialPresetNoMetallicTexture => null;

        public override bool ExtractMetallicAndSmoothness => true;

        public override bool IsCompatible(MaterialMapperContext materialMapperContext)
        {
            return base.IsCompatible(materialMapperContext) && (materialMapperContext == null || materialMapperContext.Material?.UsesRoughnessSetup == true);
        }

        protected override IEnumerable ApplyGlossinessMapTexture(TextureLoadingContext textureLoadingContext)
        {
            if (textureLoadingContext.UnityTexture != null)
            {
                textureLoadingContext.Context.AddUsedTexture(textureLoadingContext.UnityTexture);
            }
            textureLoadingContext.MaterialMapperContext.VirtualMaterial.SetProperty("_SpecGlossMap", textureLoadingContext.UnityTexture, GenericMaterialProperty.MetallicMap);
            if (textureLoadingContext.UnityTexture != null)
            {
                textureLoadingContext.MaterialMapperContext.VirtualMaterial.EnableKeyword("_SPECGLOSSMAP");
            }
            else
            {
                textureLoadingContext.MaterialMapperContext.VirtualMaterial.DisableKeyword("_SPECGLOSSMAP");
            }
            yield break;
        }
    }
}