#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Internationalization/Text.h"
#include "Prefab.generated.h"

UCLASS()
class BAREUEPROJECT_API APrefab : public AActor
{
	GENERATED_BODY()
public:
	APrefab ();
	APrefab (FString assetPath);
	UPROPERTY(EditAnywhere)
	FString assetPath;
};