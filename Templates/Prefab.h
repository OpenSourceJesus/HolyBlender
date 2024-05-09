#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Kismet/GameplayStatics.h"
#include "Internationalization/Text.h"
#include "Containers/Map.h"
#include "Prefab.generated.h"

UCLASS()
class BAREUEPROJECT_API APrefab : public AActor
{
	GENERATED_BODY()
public:
	APrefab ();
	APrefab (TMap<FString, FString> assetsPathsDict);
	UPROPERTY(EditAnywhere)
	TMap<FString, FString> assetsPathsDict;
};