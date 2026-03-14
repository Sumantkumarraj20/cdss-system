export type DrugBase = {
  id: string;
  name: string;
  generic_name?: string | null;
  chemical_class?: string | null;
  therapeutic_class?: string | null;
  mechanism?: string | null;
  habit_forming: boolean;
  pregnancy_category?: string | null;
  lactation_safety?: string | null;
};

export type DrugDetail = DrugBase & {
  side_effects: string[];
  diseases: string[];
  contraindications: string[];
};

export type DrugSearchResult = {
  items: DrugBase[];
  total: number;
};

export type DrugsResponse = {
  items: DrugBase[];
};

export type PresentationBundle = {
  presentation: string;
  red_flags: string[];
  differentials: string[];
  investigations: string[];
  treatments: string[];
};

export type SearchResult = {
  type: "presentation" | "diagnosis" | "symptom" | "drug" | string;
  name: string;
};

export type DecisionSupportRequest = {
  symptoms: string[];
  signs: string[];
  vitals?: Record<string, string | number> | null;
};

export type DecisionSupportResponse = {
  suggestions: string[];
  ranked_differentials: string[];
};
