using System;
using System.Collections;
using TriLibCore.General;
using UnityEngine;

namespace TriLibCore.Mappers
{
    /// <summary>Represents a Material Mapper that converts TriLib Materials into Unity Standard Materials.</summary>
    [Serializable]
    [CreateAssetMenu(menuName = "TriLib/Mappers/Material/Standard Material Mapper", fileName = "StandardMaterialMapper")]
    public class StandardMaterialMapper : MaterialMapper
    {
        public bool ForceShaderVariantCollection;

        public override bool UseShaderVariantCollection => ForceShaderVariantCollection;

        public override string ShaderVariantCollectionPath => "Materials/Standard/StandardShaderVariantCollection";

        public override Shader VariantCollectionShader => Shader.Find("Standard");

        #region Standard
        public override Material MaterialPreset => Resources.Load<Material>("Materials/Standard/Standard/TriLibStandard");

        public override Material CutoutMaterialPreset => Resources.Load<Material>("Materials/Standard/Standard/TriLibStandardAlphaCutout");

        public override Material TransparentComposeMaterialPreset => Resources.Load<Material>("Materials/Standard/Standard/TriLibStandardAlphaCompose");

        public override Material TransparentMaterialPreset => Resources.Load<Material>("Materials/Standard/Standard/TriLibStandardAlpha");

        public override Material MaterialPresetNoMetallicTexture => Resources.Load<Material>("Materials/Standard/Standard/TriLibStandardNoMetallicTexture");

        public override Material CutoutMaterialPresetNoMetallicTexture => Resources.Load<Material>("Materials/Standard/Standard/TriLibStandardAlphaCutoutNoMetallicTexture");

        public override Material TransparentMaterialPresetNoMetallicTexture => Resources.Load<Material>("Materials/Standard/Standard/TriLibStandardAlphaNoMetallicTexture");

        public override Material TransparentComposeMaterialPresetNoMetallicTexture => TransparentComposeMaterialPreset;
        #endregion

        public override Material LoadingMaterial => Resources.Load<Material>("Materials/Standard/TriLibStandardLoading");

        public override bool ExtractMetallicAndSmoothness
        {
            get
            {
                return false;
            }
        }

        public override bool IsCompatible(MaterialMapperContext materialMapperContext)
        {
            return TriLibSettings.GetBool("StandardMaterialMapper", false);
        }

        public override bool UsesCoroutines => true;

        public override IEnumerable MapCoroutine(MaterialMapperContext materialMapperContext)
        {
            materialMapperContext.VirtualMaterial = new VirtualMaterial();

            foreach (var item in CheckTransparencyMapTexture(materialMapperContext))
            {
                yield return item;
            }
            foreach (var item in CheckSpecularMapTexture(materialMapperContext))
            {
                yield return item;
            }
            foreach (var item in CheckDiffuseMapTexture(materialMapperContext))
            {
                yield return item;
            }
            foreach (var item in CheckDiffuseColor(materialMapperContext))
            {
                yield return item;
            }
            foreach (var item in CheckNormalMapTexture(materialMapperContext))
            {
                yield return item;
            }
            foreach (var item in CheckEmissionColor(materialMapperContext))
            {
                yield return item;
            }
            foreach (var item in CheckEmissionMapTexture(materialMapperContext))
            {
                yield return item;
            }
            foreach (var item in CheckOcclusionMapTexture(materialMapperContext))
            {
                yield return item;
            }
            foreach (var item in CheckGlossinessMapTexture(materialMapperContext))
            {
                yield return item;
            }
            foreach (var item in CheckGlossinessValue(materialMapperContext))
            {
                yield return item;
            }
            foreach (var item in CheckMetallicGlossMapTexture(materialMapperContext))
            {
                yield return item;
            }
            foreach (var item in CheckMetallicValue(materialMapperContext))
            {
                yield return item;
            }
            if (materialMapperContext.Context.Options.LoadDisplacementTextures)
            {
                foreach (var item in CheckDisplacementTexture(materialMapperContext))
                {
                    yield return item;
                }
            }
            BuildMaterial(materialMapperContext);
        }

        private IEnumerable CheckDiffuseMapTexture(MaterialMapperContext materialMapperContext)
        {
            var diffuseTexturePropertyName = materialMapperContext.Material.GetGenericPropertyName(GenericMaterialProperty.DiffuseMap);
            var textureValue = materialMapperContext.Material.GetTextureValue(diffuseTexturePropertyName);
            foreach (var item in LoadTextureWithCoroutineCallbacks(materialMapperContext, TextureType.Diffuse, textureValue, CheckTextureOffsetAndScalingCoroutine, ApplyDiffuseMapTexture))
            {
                yield return item;
            }
        }

        private IEnumerable ApplyDiffuseMapTexture(TextureLoadingContext textureLoadingContext)
        {
            if (textureLoadingContext.UnityTexture != null)
            {
                textureLoadingContext.Context.AddUsedTexture(textureLoadingContext.UnityTexture);
            }
            textureLoadingContext.MaterialMapperContext.VirtualMaterial.SetProperty("_MainTex", textureLoadingContext.UnityTexture, GenericMaterialProperty.DiffuseMap);
            yield break;
        }

        private IEnumerable CheckGlossinessValue(MaterialMapperContext materialMapperContext)
        {
            var value = materialMapperContext.Material.GetGenericFloatValueMultiplied(GenericMaterialProperty.Glossiness, materialMapperContext);
            materialMapperContext.VirtualMaterial.SetProperty("_Glossiness", value);
            materialMapperContext.VirtualMaterial.SetProperty("_GlossMapScale", value);
            yield break;
        }

        private IEnumerable CheckMetallicValue(MaterialMapperContext materialMapperContext)
        {
            var value = materialMapperContext.Material.GetGenericFloatValueMultiplied(GenericMaterialProperty.Metallic, materialMapperContext);
            materialMapperContext.VirtualMaterial.SetProperty("_Metallic", value);
            yield break;
        }

        private IEnumerable CheckEmissionMapTexture(MaterialMapperContext materialMapperContext)
        {
            var emissionTexturePropertyName = materialMapperContext.Material.GetGenericPropertyName(GenericMaterialProperty.EmissionMap);
            var textureValue = materialMapperContext.Material.GetTextureValue(emissionTexturePropertyName);
            foreach (var item in LoadTextureWithCoroutineCallbacks(materialMapperContext, TextureType.Emission, textureValue, CheckTextureOffsetAndScalingCoroutine, ApplyEmissionMapTexture))
            {
                yield return item;
            }
        }

        private IEnumerable ApplyEmissionMapTexture(TextureLoadingContext textureLoadingContext)
        {
            if (textureLoadingContext.UnityTexture == null && textureLoadingContext.MaterialMapperContext.VirtualMaterial.HasEmissionColor)
            {
                textureLoadingContext.OriginalUnityTexture = textureLoadingContext.UnityTexture = TriLibCore.Textures.DefaultTextures.White;
            }
            if (textureLoadingContext.UnityTexture != null)
            {
                textureLoadingContext.Context.AddUsedTexture(textureLoadingContext.UnityTexture);
            }
            textureLoadingContext.MaterialMapperContext.VirtualMaterial.SetProperty("_EmissionMap", textureLoadingContext.UnityTexture, GenericMaterialProperty.EmissionMap);
            if (textureLoadingContext.UnityTexture != null)
            {
                textureLoadingContext.MaterialMapperContext.VirtualMaterial.EnableKeyword("_EMISSION");
                textureLoadingContext.MaterialMapperContext.VirtualMaterial.GlobalIlluminationFlags = MaterialGlobalIlluminationFlags.RealtimeEmissive;
            }
            else
            {
                textureLoadingContext.MaterialMapperContext.VirtualMaterial.DisableKeyword("_EMISSION");
                textureLoadingContext.MaterialMapperContext.VirtualMaterial.GlobalIlluminationFlags = MaterialGlobalIlluminationFlags.EmissiveIsBlack;
            }
            yield break;
        }

        private IEnumerable CheckNormalMapTexture(MaterialMapperContext materialMapperContext)
        {
            var normalMapTexturePropertyName = materialMapperContext.Material.GetGenericPropertyName(GenericMaterialProperty.NormalMap);
            var textureValue = materialMapperContext.Material.GetTextureValue(normalMapTexturePropertyName);
            foreach (var item in LoadTextureWithCoroutineCallbacks(materialMapperContext, TextureType.NormalMap, textureValue, CheckTextureOffsetAndScalingCoroutine, ApplyNormalMapTexture))
            {
                yield return item;
            }
        }

        private IEnumerable ApplyNormalMapTexture(TextureLoadingContext textureLoadingContext)
        {
            if (textureLoadingContext.UnityTexture != null)
            {
                textureLoadingContext.Context.AddUsedTexture(textureLoadingContext.UnityTexture);
            }
            textureLoadingContext.MaterialMapperContext.VirtualMaterial.SetProperty("_BumpMap", textureLoadingContext.UnityTexture, GenericMaterialProperty.NormalMap);
            if (textureLoadingContext.UnityTexture != null)
            {
                textureLoadingContext.MaterialMapperContext.VirtualMaterial.EnableKeyword("_NORMALMAP");
                var normalStrengthPropertyName = textureLoadingContext.MaterialMapperContext.Material.GetGenericPropertyName(GenericMaterialProperty.NormalStrength);
                if (textureLoadingContext.MaterialMapperContext.Material.HasProperty(normalStrengthPropertyName))
                {
                    var normalStrength = textureLoadingContext.MaterialMapperContext.Material.GetGenericFloatValueMultiplied(GenericMaterialProperty.NormalStrength, textureLoadingContext.MaterialMapperContext);
                    textureLoadingContext.MaterialMapperContext.VirtualMaterial.SetProperty("_BumpScale", normalStrength);
                }
                else
                {
                    textureLoadingContext.MaterialMapperContext.VirtualMaterial.SetProperty("_BumpScale", 1f);
                }
            }
            else
            {
                textureLoadingContext.MaterialMapperContext.VirtualMaterial.DisableKeyword("_NORMALMAP");
            }
            yield break;
        }

        private IEnumerable CheckTransparencyMapTexture(MaterialMapperContext materialMapperContext)
        {
            materialMapperContext.VirtualMaterial.HasAlpha |= materialMapperContext.Material.UsesAlpha;
            var transparencyTexturePropertyName = materialMapperContext.Material.GetGenericPropertyName(GenericMaterialProperty.TransparencyMap);
            var textureValue = materialMapperContext.Material.GetTextureValue(transparencyTexturePropertyName);
            foreach (var item in LoadTextureWithCoroutineCallbacks(materialMapperContext, TextureType.Transparency, textureValue, CheckTextureOffsetAndScalingCoroutine))
            {
                yield return item;
            }
        }

        private IEnumerable CheckSpecularMapTexture(MaterialMapperContext materialMapperContext)
        {
            var specularTexturePropertyName = materialMapperContext.Material.GetGenericPropertyName(GenericMaterialProperty.SpecularMap);
            var textureValue = materialMapperContext.Material.GetTextureValue(specularTexturePropertyName);
            foreach (var item in LoadTextureWithCoroutineCallbacks(materialMapperContext, TextureType.Specular, textureValue, CheckTextureOffsetAndScalingCoroutine))
            {
                yield return item;
            }
        }

        private IEnumerable CheckOcclusionMapTexture(MaterialMapperContext materialMapperContext)
        {
            var occlusionMapTextureName = materialMapperContext.Material.GetGenericPropertyName(GenericMaterialProperty.OcclusionMap);
            var textureValue = materialMapperContext.Material.GetTextureValue(occlusionMapTextureName);
            foreach (var item in LoadTextureWithCoroutineCallbacks(materialMapperContext, TextureType.Occlusion, textureValue, CheckTextureOffsetAndScalingCoroutine, ApplyOcclusionMapTexture))
            {
                yield return item;
            }
        }

        private IEnumerable ApplyOcclusionMapTexture(TextureLoadingContext textureLoadingContext)
        {
            if (textureLoadingContext.Texture != null)
            {
                textureLoadingContext.Context.AddUsedTexture(textureLoadingContext.UnityTexture);
            }
            textureLoadingContext.MaterialMapperContext.VirtualMaterial.SetProperty("_OcclusionMap", textureLoadingContext.UnityTexture, GenericMaterialProperty.OcclusionMap);
            if (textureLoadingContext.UnityTexture != null)
            {
                textureLoadingContext.MaterialMapperContext.VirtualMaterial.EnableKeyword("_OCCLUSIONMAP");
            }
            else
            {
                textureLoadingContext.MaterialMapperContext.VirtualMaterial.DisableKeyword("_OCCLUSIONMAP");
            }
            yield break;
        }

        private IEnumerable CheckGlossinessMapTexture(MaterialMapperContext materialMapperContext)
        {
            var auxiliaryMapTextureName = materialMapperContext.Material.GetGenericPropertyName(GenericMaterialProperty.GlossinessOrRoughnessMap);
            var textureValue = materialMapperContext.Material.GetTextureValue(auxiliaryMapTextureName);
            foreach (var item in LoadTextureWithCoroutineCallbacks(materialMapperContext, TextureType.GlossinessOrRoughness, textureValue, CheckTextureOffsetAndScalingCoroutine, ApplyGlossinessMapTexture))
            {
                yield return item;
            }
        }

        private IEnumerable CheckMetallicGlossMapTexture(MaterialMapperContext materialMapperContext)
        {
            var metallicGlossMapTextureName = materialMapperContext.Material.GetGenericPropertyName(GenericMaterialProperty.MetallicMap);
            var textureValue = materialMapperContext.Material.GetTextureValue(metallicGlossMapTextureName);
            foreach (var item in LoadTextureWithCoroutineCallbacks(materialMapperContext, TextureType.Metalness, textureValue, CheckTextureOffsetAndScalingCoroutine, ApplyMetallicGlossMapTexture))
            {
                yield return item;
            }
        }

        private IEnumerable CheckDisplacementTexture(MaterialMapperContext materialMapperContext)
        {
            var displacementMapTextureName = materialMapperContext.Material.GetGenericPropertyName(GenericMaterialProperty.DisplacementMap);
            var textureValue = materialMapperContext.Material.GetTextureValue(displacementMapTextureName);
            foreach (var item in LoadTextureWithCoroutineCallbacks(materialMapperContext, TextureType.Displacement, textureValue, CheckTextureOffsetAndScalingCoroutine, ApplyDisplacementTexture))
            {
                yield return item;
            }
        }

        protected virtual IEnumerable ApplyGlossinessMapTexture(TextureLoadingContext textureLoadingContext)
        {
            yield break;
        }

        private IEnumerable ApplyMetallicGlossMapTexture(TextureLoadingContext textureLoadingContext)
        {
            if (textureLoadingContext.UnityTexture != null)
            {
                textureLoadingContext.Context.AddUsedTexture(textureLoadingContext.UnityTexture);
            }
            textureLoadingContext.MaterialMapperContext.VirtualMaterial.SetProperty("_MetallicGlossMap", textureLoadingContext.UnityTexture, GenericMaterialProperty.MetallicMap);
            if (textureLoadingContext.UnityTexture != null)
            {
                textureLoadingContext.MaterialMapperContext.VirtualMaterial.EnableKeyword("_METALLICGLOSSMAP");
            }
            else
            {
                textureLoadingContext.MaterialMapperContext.VirtualMaterial.DisableKeyword("_METALLICGLOSSMAP");
            }
            yield break;
        }

        private IEnumerable ApplyDisplacementTexture(TextureLoadingContext textureLoadingContext)
        {
            if (textureLoadingContext.UnityTexture != null)
            {
                textureLoadingContext.Context.AddUsedTexture(textureLoadingContext.UnityTexture);
            }
            textureLoadingContext.MaterialMapperContext.VirtualMaterial.SetProperty("_ParallaxMap", textureLoadingContext.UnityTexture, GenericMaterialProperty.DisplacementMap);
            if (textureLoadingContext.UnityTexture != null)
            {
                textureLoadingContext.MaterialMapperContext.VirtualMaterial.EnableKeyword("_PARALLAXMAP");
                var displacementStrengthPropertyName = textureLoadingContext.MaterialMapperContext.Material.GetGenericPropertyName(GenericMaterialProperty.DisplacementStrength);
                if (textureLoadingContext.MaterialMapperContext.Material.HasProperty(displacementStrengthPropertyName))
                {
                    var normalStrength = textureLoadingContext.MaterialMapperContext.Material.GetGenericFloatValueMultiplied(GenericMaterialProperty.DisplacementStrength, textureLoadingContext.MaterialMapperContext);
                    textureLoadingContext.MaterialMapperContext.VirtualMaterial.SetProperty("_Parallax", normalStrength);
                }
                else
                {
                    textureLoadingContext.MaterialMapperContext.VirtualMaterial.SetProperty("_Parallax", 0f);
                }
            }
            else
            {
                textureLoadingContext.MaterialMapperContext.VirtualMaterial.DisableKeyword("_PARALLAXMAP");
            }
            yield break;
        }

        private IEnumerable CheckEmissionColor(MaterialMapperContext materialMapperContext)
        {
            var value = materialMapperContext.Material.GetGenericColorValueMultiplied(GenericMaterialProperty.EmissionColor, materialMapperContext);
            materialMapperContext.VirtualMaterial.SetProperty("_EmissionColor", materialMapperContext.Context.Options.ApplyGammaCurveToMaterialColors ? value.gamma : value);
            if (value != Color.black)
            {
                materialMapperContext.VirtualMaterial.EnableKeyword("_EMISSION");
                materialMapperContext.VirtualMaterial.GlobalIlluminationFlags = MaterialGlobalIlluminationFlags.RealtimeEmissive;
                materialMapperContext.VirtualMaterial.SetProperty("_EmissiveIntensity", 1f);
                materialMapperContext.VirtualMaterial.HasEmissionColor = true;
            }
            else
            {
                materialMapperContext.VirtualMaterial.DisableKeyword("_EMISSION");
                materialMapperContext.VirtualMaterial.GlobalIlluminationFlags = MaterialGlobalIlluminationFlags.EmissiveIsBlack;
            }
            yield break;
        }

        private IEnumerable CheckDiffuseColor(MaterialMapperContext materialMapperContext)
        {
            var value = materialMapperContext.Material.GetGenericColorValueMultiplied(GenericMaterialProperty.DiffuseColor, materialMapperContext);
            value.a *= materialMapperContext.Material.GetGenericFloatValueMultiplied(GenericMaterialProperty.AlphaValue);
            materialMapperContext.VirtualMaterial.HasAlpha |= value.a < 1f;
            materialMapperContext.VirtualMaterial.SetProperty("_Color", materialMapperContext.Context.Options.ApplyGammaCurveToMaterialColors ? value.gamma : value);
            yield break;
        }

        public override string GetDiffuseTextureName(MaterialMapperContext materialMapperContext)
        {
            return "_MainTex";
        }

        public override string GetGlossinessOrRoughnessTextureName(MaterialMapperContext materialMapperContext)
        {
            return "_MetallicGlossMap";
        }

        public override string GetDiffuseColorName(MaterialMapperContext materialMapperContext)
        {
            return "_Color";
        }

        public override string GetEmissionColorName(MaterialMapperContext materialMapperContext)
        {
            return "_EmissionColor";
        }

        public override string GetGlossinessOrRoughnessName(MaterialMapperContext materialMapperContext)
        {
            return "_GlossMapScale";
        }

        public override string GetMetallicName(MaterialMapperContext materialMapperContext)
        {
            return "_Metallic";
        }

        public override string GetMetallicTextureName(MaterialMapperContext materialMapperContext)
        {
            return null;
        }
    }
}
