import { RegionInfoService1, RegionInfoServiceMock } from '../services/implementations/region_info_service';

// // Création du contexte pour l'injection de dépendances
// export const RegionInfoServiceContext = createContext<IRegionService>(new RegionInfoService1());

// Hook personnalisé pour utiliser le service
export const RegionInfoController = () => {
    return new RegionInfoService1();
};