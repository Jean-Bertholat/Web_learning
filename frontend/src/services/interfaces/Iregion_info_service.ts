import { RegionInfo } from "../schemas/region_resp_schema";

export interface IRegionService {
    get_region_info(region_id: number): Promise<RegionInfo>;
}

