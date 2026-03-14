export type BaseDoc = {
  id: string;
  name: string;
  updated_at: string;
  is_deleted: boolean;
};

export type DrugDoc = BaseDoc & {
  generic_name?: string;
  chemical_class?: string;
  therapeutic_class?: string;
  mechanism?: string;
  habit_forming?: boolean;
  pregnancy_category?: string;
  lactation_safety?: string;
};

export type DiagnosisDoc = BaseDoc & {
  icd10_code?: string;
  description?: string;
  evidence_grade?: string;
};

export type PresentationDoc = BaseDoc & {
  summary?: string;
  guideline_source?: string;
  description?: string;
};

export type SymptomDoc = BaseDoc & {
  description?: string;
};

export const baseProperties = {
  id: { type: "string", maxLength: 64, primary: true },
  name: { type: "string" },
  updated_at: { type: "string", format: "date-time" },
  is_deleted: { type: "boolean", default: false },
};

export const drugSchema = {
  title: "drug",
  version: 0,
  primaryKey: "id",
  type: "object",
  properties: {
    ...baseProperties,
    generic_name: { type: "string" },
    chemical_class: { type: "string" },
    therapeutic_class: { type: "string" },
    mechanism: { type: "string" },
    habit_forming: { type: "boolean" },
    pregnancy_category: { type: "string" },
    lactation_safety: { type: "string" },
  },
  required: ["id", "name", "updated_at", "is_deleted"],
  indexes: ["updated_at", "is_deleted"],
} as const;

export const diagnosisSchema = {
  title: "diagnosis",
  version: 0,
  primaryKey: "id",
  type: "object",
  properties: {
    ...baseProperties,
    icd10_code: { type: "string" },
    description: { type: "string" },
    evidence_grade: { type: "string" },
  },
  required: ["id", "name", "updated_at", "is_deleted"],
  indexes: ["updated_at", "is_deleted"],
} as const;

export const presentationSchema = {
  title: "presentation",
  version: 0,
  primaryKey: "id",
  type: "object",
  properties: {
    ...baseProperties,
    summary: { type: "string" },
    guideline_source: { type: "string" },
    description: { type: "string" },
  },
  required: ["id", "name", "updated_at", "is_deleted"],
  indexes: ["updated_at", "is_deleted"],
} as const;

export const symptomSchema = {
  title: "symptom",
  version: 0,
  primaryKey: "id",
  type: "object",
  properties: {
    ...baseProperties,
    description: { type: "string" },
  },
  required: ["id", "name", "updated_at", "is_deleted"],
  indexes: ["updated_at", "is_deleted"],
} as const;

export const collections = {
  drugs: { schema: drugSchema },
  diagnoses: { schema: diagnosisSchema },
  presentations: { schema: presentationSchema },
  symptoms: { schema: symptomSchema },
} as const;
