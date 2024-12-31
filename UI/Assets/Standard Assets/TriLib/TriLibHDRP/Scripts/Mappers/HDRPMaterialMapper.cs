using System;
using System.Collections;
using TriLibCore.General;
using TriLibCore.Mappers;
using UnityEngine;
using UnityEngine.Experimental.Rendering;

namespace TriLibCore.HDRP.Mappers
{
    /// <summary>Represents a Material Mapper that converts TriLib Materials into Unity HDRP Materials.</summary>
    [Serializable]
    [CreateAssetMenu(menuName = "TriLib/Mappers/Material/HDRP Material Mapper", fileName = "HDRPMaterialMapper")]
    public class HDRPMaterialMapper : MaterialMapper
    {
        public bool ForceShaderVariantCollection;

        public override bool UseShaderVariantCollection => ForceShaderVariantCollection;

        public override string ShaderVariantCollectionPath => "Materials/HDRP/HDRPVariantCollection";

        public override Shader VariantCollectionShader => Shader.Find("HDRP/Lit");
        #region Standard
        public override Material MaterialPreset => Resources.Load<Material>("Materials/HDRP/Standard/TriLibHDRP");

        public override Material CutoutMaterialPreset => Resources.Load<Material>("Materials/HDRP/Standard/TriLibHDRPAlphaCutout");

        public override Material TransparentMaterialPreset => Resources.Load<Material>("Materials/HDRP/Standard/TriLibHDRPAlpha");

        public override Material TransparentComposeMaterialPreset => Resources.Load<Material>("Materials/HDRP/Standard/TriLibHDRPAlpha");
        #endregion

        public override Material LoadingMaterial => Resources.Load<Material>("Materials/HDRP/TriLibHDRPLoading");

        public override bool ExtractMetallicAndSmoothness => false;
        public override bool UsesCoroutines => true;

        public override bool IsCompatible(MaterialMapperContext materialMapperContext)
        {
            return TriLibSettings.GetBool("HDRPMaterialMapper", false);
        }

        public override IEnumerable MapCoroutine(MaterialMapperContext materialMapperContext)
        {
            materialMapperContext.VirtualMaterial = new HDRPVirtualMaterial();

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
            BuildMaterial(materialMapperContext);
            foreach (var item in BuildHDRPMask(materialMapperContext))
            {
                yield return item;
            }
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
            textureLoadingContext.MaterialMapperContext.VirtualMaterial.SetProperty("_BaseColorMap", textureLoadingContext.UnityTexture, GenericMaterialProperty.DiffuseMap);
            yield break;
        }

        private IEnumerable CheckGlossinessValue(MaterialMapperContext materialMapperContext)
        {
            var value = materialMapperContext.Material.GetGenericFloatValueMultiplied(GenericMaterialProperty.Glossiness, materialMapperContext);
            materialMapperContext.VirtualMaterial.SetProperty("_Smoothness", value);
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
            textureLoadingContext.MaterialMapperContext.VirtualMaterial.SetProperty("_EmissiveColorMap", textureLoadingContext.UnityTexture, GenericMaterialProperty.EmissionMap);
            if (textureLoadingContext.UnityTexture)
            {
                textureLoadingContext.MaterialMapperContext.VirtualMaterial.EnableKeyword("_EMISSIVE_COLOR_MAP");
                textureLoadingContext.MaterialMapperContext.VirtualMaterial.GlobalIlluminationFlags = MaterialGlobalIlluminationFlags.RealtimeEmissive;
                textureLoadingContext.MaterialMapperContext.VirtualMaterial.SetProperty("_EmissiveIntensity", 1f);
            }
            else
            {
                textureLoadingContext.MaterialMapperContext.VirtualMaterial.DisableKeyword("_EMISSIVE_COLOR_MAP");
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
            textureLoadingContext.MaterialMapperContext.VirtualMaterial.SetProperty("_NormalMap", textureLoadingContext.UnityTexture, GenericMaterialProperty.NormalMap);
            if (textureLoadingContext.UnityTexture != null)
            {
                textureLoadingContext.MaterialMapperContext.VirtualMaterial.EnableKeyword("_NORMALMAP");
                textureLoadingContext.MaterialMapperContext.VirtualMaterial.EnableKeyword("_NORMALMAP_TANGENT_SPACE");
                textureLoadingContext.MaterialMapperContext.VirtualMaterial.SetProperty("_NormalScale", 1f);
            }
            else
            {
                textureLoadingContext.MaterialMapperContext.VirtualMaterial.DisableKeyword("_NORMALMAP");
                textureLoadingContext.MaterialMapperContext.VirtualMaterial.DisableKeyword("_NORMALMAP_TANGENT_SPACE");
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
            ((HDRPVirtualMaterial)textureLoadingContext.MaterialMapperContext.VirtualMaterial).OcclusionTexture = textureLoadingContext.UnityTexture;
            yield break;
        }

        private IEnumerable CheckGlossinessMapTexture(MaterialMapperContext materialMapperContext)
        {
            var auxiliaryMapTextureName = materialMapperContext.Material.GetGenericPropertyName(GenericMaterialProperty.GlossinessOrRoughnessMap);
            var textureValue = materialMapperContext.Material.GetTextureValue(auxiliaryMapTextureName);
            foreach (var item in LoadTextureWithCoroutineCallbacks(materialMapperContext, TextureType.GlossinessOrRoughness, textureValue, CheckTextureOffsetAndScalingCoroutine))
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

        private IEnumerable ApplyMetallicGlossMapTexture(TextureLoadingContext textureLoadingContext)
        {
            ((HDRPVirtualMaterial)textureLoadingContext.MaterialMapperContext.VirtualMaterial).MetallicTexture = textureLoadingContext.UnityTexture;
            yield break;
        }

        private IEnumerable CheckEmissionColor(MaterialMapperContext materialMapperContext)
        {
            var value = materialMapperContext.Material.GetGenericColorValueMultiplied(GenericMaterialProperty.EmissionColor, materialMapperContext);
            materialMapperContext.VirtualMaterial.SetProperty("_EmissiveColor", materialMapperContext.Context.Options.ApplyGammaCurveToMaterialColors ? value.gamma : value);
            materialMapperContext.VirtualMaterial.SetProperty("_EmissiveColorLDR", materialMapperContext.Context.Options.ApplyGammaCurveToMaterialColors ? value.gamma : value);
            if (value != Color.black)
            {
                materialMapperContext.VirtualMaterial.GlobalIlluminationFlags = MaterialGlobalIlluminationFlags.RealtimeEmissive;
                materialMapperContext.VirtualMaterial.SetProperty("_EmissiveIntensity", 1f);
                materialMapperContext.VirtualMaterial.HasEmissionColor = true;
            }
            else
            {
                materialMapperContext.VirtualMaterial.GlobalIlluminationFlags = MaterialGlobalIlluminationFlags.EmissiveIsBlack;
            }

            yield break;
        }

        private IEnumerable CheckDiffuseColor(MaterialMapperContext materialMapperContext)
        {
            var value = materialMapperContext.Material.GetGenericColorValueMultiplied(GenericMaterialProperty.DiffuseColor, materialMapperContext);
            value.a *= materialMapperContext.Material.GetGenericFloatValueMultiplied(GenericMaterialProperty.AlphaValue);
            materialMapperContext.VirtualMaterial.HasAlpha |= value.a < 1f;
            materialMapperContext.VirtualMaterial.SetProperty("_BaseColor", materialMapperContext.Context.Options.ApplyGammaCurveToMaterialColors ? value.gamma : value);
            materialMapperContext.VirtualMaterial.SetProperty("_Color", materialMapperContext.Context.Options.ApplyGammaCurveToMaterialColors ? value.gamma : value);
            yield break;
        }

        private IEnumerable BuildHDRPMask(MaterialMapperContext materialMapperContext)
        {
            materialMapperContext.Completed = false;
            if (materialMapperContext.UnityMaterial == null)
            {
                yield break;
            }
            var hdrpVirtualMaterial = (HDRPVirtualMaterial)materialMapperContext.VirtualMaterial;
            var maskBaseTexture = hdrpVirtualMaterial.MetallicTexture ?? hdrpVirtualMaterial.OcclusionTexture ?? hdrpVirtualMaterial.DetailMaskTexture;
            if (maskBaseTexture == null)
            {
                if (materialMapperContext.Context.Options.UseMaterialKeywords)
                {
                    materialMapperContext.UnityMaterial.DisableKeyword("_MASKMAP");
                }
                yield break;
            }
            var graphicsFormat = GraphicsFormat.R8G8B8A8_UNorm;
            var renderTexture = new RenderTexture(maskBaseTexture.width, maskBaseTexture.height, 0, graphicsFormat);
            renderTexture.name = $"{(string.IsNullOrWhiteSpace(maskBaseTexture.name) ? "Unnamed" : maskBaseTexture.name)}_Mask";
            renderTexture.useMipMap = false;
            renderTexture.autoGenerateMips = false;
            var material = new Material(Shader.Find("Hidden/TriLib/BuildHDRPMask"));
            if (hdrpVirtualMaterial.MetallicTexture != null)
            {
                material.SetTexture("_MetallicTex", hdrpVirtualMaterial.MetallicTexture);
            }
            if (hdrpVirtualMaterial.OcclusionTexture != null)
            {
                material.SetTexture("_OcclusionTex", hdrpVirtualMaterial.OcclusionTexture);
            }
            if (hdrpVirtualMaterial.DetailMaskTexture != null)
            {
                material.SetTexture("_DetailMaskTex", hdrpVirtualMaterial.DetailMaskTexture);
            }
            Graphics.Blit(null, renderTexture, material);
            if (renderTexture.useMipMap)
            {
                renderTexture.GenerateMips();
            }
            if (materialMapperContext.Context.Options.UseMaterialKeywords)
            {
                materialMapperContext.UnityMaterial.EnableKeyword("_MASKMAP");
            }
            materialMapperContext.UnityMaterial.SetTexture("_MaskMap", renderTexture);
            materialMapperContext.VirtualMaterial.TextureProperties.Add("_MaskMap", renderTexture);
            if (Application.isPlaying)
            {
                Destroy(material);
            }
            else
            {
                DestroyImmediate(material);
            }
            materialMapperContext.Completed = true;
            foreach (var item in materialMapperContext.Context.ReleaseMainThread())
            {
                yield return item;
            }
        }

        public override string GetDiffuseTextureName(MaterialMapperContext materialMapperContext)
        {
            return "_BaseColorMap";
        }

        public override string GetGlossinessOrRoughnessTextureName(MaterialMapperContext materialMapperContext)
        {
            return "_MetallicGlossMap";
        }

        public override string GetDiffuseColorName(MaterialMapperContext materialMapperContext)
        {
            return "_BaseColor";
        }

        public override string GetEmissionColorName(MaterialMapperContext materialMapperContext)
        {
            return "_EmissionColor";
        }

        public override string GetGlossinessOrRoughnessName(MaterialMapperContext materialMapperContext)
        {
            return "_Smoothness";
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
